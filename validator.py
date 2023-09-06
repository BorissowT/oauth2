import json
import logging
from urllib.request import urlopen
import requests

from authlib.jose import JoseError, jwt
from authlib.oauth2.rfc6750 import BearerTokenValidator, InvalidTokenError, \
    InsufficientScopeError
from authlib.jose.rfc7517.jwk import JsonWebKey
from authlib.oauth2.rfc7523 import JWTBearerToken

logger = logging.getLogger(__name__)


class KeyCloakJWTBearerTokenValidator(BearerTokenValidator):
    """Validation class. Must be injected at ResourceProtector."""
    TOKEN_TYPE = 'bearer'
    token_cls = JWTBearerToken
    client_id = None
    issuer = None

    def __init__(self,
                 issuer: str,
                 realm: str,
                 client_id: str,
                 **extra_attributes):
        """Configure claims for Bearer Token Validator and for jwt decode.
         Retrieve public key from key cloak.

        :param issuer: keycloak url.
                    example(http://192.168.105.139:8080/auth/realms/myrealm)
        :param realm: keycloak realm
        :param client_id: client_id of protected resource(api)
        :param client_secret: client secret of protected resource(api)
        :param extra_attributes:
        """
        self.client_id = client_id
        self.issuer = issuer
        jsonurl = urlopen(f"{issuer}/protocol/openid-connect/certs")
        public_key = JsonWebKey.import_key_set(json.loads(jsonurl.read()))
        super(KeyCloakJWTBearerTokenValidator, self).__init__(
                                                        realm,
                                                        **extra_attributes)
        self.public_key = public_key
        claims_options = {
            'exp': {'essential': True},
            'client_id': {'essential': False},
            'grant_type': {'essential': False},
        }
        # if issuer:
        #     # TODO Issuer is turned off so any react app
        #     #  in network can access it
        #     claims_options['iss'] = {'essential': True, 'value': issuer}
        self.claims_options = claims_options

    def authenticate_token(self, token_string):
        """Authenticate access token with public key defined by auth server.

        :param token_string: access token in string.
        :return: JWT Token object
        """
        try:
            token = jwt.decode(
                token_string, self.public_key,
                claims_options=self.claims_options,
                claims_cls=self.token_cls,
            )
            token.validate()
            return token
        except JoseError as error:
            logger.debug('Authenticate token failed. %r', error)
            return None

    def validate_token(self,
                       access_token,
                       access_token_string: str,
                       request,
                       resource: str = None,
                       scopes: list[str] = None):
        """Check if token is active and matches the requested scopes
        and resources

        :param access_token: access token issued by key cloak
        :param request: Flask context request
        :param resource: keycloak resource
        :param scopes: scopes allowed for particular resource
        :return:
        """
        if not access_token:
            raise InvalidTokenError(realm=self.realm,
                                    extra_attributes=self.extra_attributes)
        if access_token.is_expired():
            raise InvalidTokenError(realm=self.realm,
                                    extra_attributes=self.extra_attributes)
        if access_token.is_revoked():
            raise InvalidTokenError(realm=self.realm,
                                    extra_attributes=self.extra_attributes)
        if self.scope_insufficient(access_token_string=access_token_string,
                                   required_resource=resource,
                                   required_scopes=scopes):
            raise InsufficientScopeError()

    def scope_insufficient(self,
                           access_token_string: str = None,
                           required_resource: str = None,
                           required_scopes: list[str] = None) -> bool:
        """Check if scope and resources are sufficient. Return True if
        scope is not sufficient.

        :param access_token_string: access token issued by key cloak in string
        :param required_resource: required resource for endpoint
        :param required_scopes: required scopes for endpoint
        :return: bool True if insufficient
        """
        user_permissions = self.get_rpt_permissions(access_token_string)
        for permission in user_permissions:
            if permission['rsname'] == required_resource:
                for scope in permission['scopes']:
                    if scope in required_scopes:
                        return False
        return True

    def execute_rpt_call(self, access_token_string: str):
        """Make request POST call to RPT endpoint. Return access token

        :param access_token_string:
        :return: token in string
        """
        url = self.issuer + "/protocol/openid-connect/token"
        headers = {
            "Authorization": "Bearer " + access_token_string,
            # Replace with your access token
            "Content-Type": "application/x-www-form-urlencoded"
            # Assuming a form-urlencoded request
        }
        data = {
            "grant_type": "urn:ietf:params:oauth:grant-type:uma-ticket",
            "audience": self.client_id
        }
        response = requests.post(url, headers=headers, data=data)
        return response.json()["access_token"]

    def get_rpt_permissions(self, access_token_string: str):
        """Execute RPT call and extract all permissions of a user in jwt
         access token.

        :param access_token_string:
        :return: dict with permissions
        """

        rpt_access_token = self.execute_rpt_call(access_token_string)
        user_permissions = self.extract_permissions(rpt_access_token)
        return user_permissions["permissions"]

    def extract_permissions(self, rpt_access_token):
        """Decode jwt token and extract authorisation claim.

        :param rpt_access_token: access string token
        :return:
        """
        token = jwt.decode(
            rpt_access_token, self.public_key,
            claims_options=self.claims_options,
            claims_cls=self.token_cls,
        )
        return token['authorization']
