import json
import logging
from urllib.request import urlopen

from authlib.jose import JoseError, jwt
from authlib.oauth2.rfc6750 import BearerTokenValidator
from authlib.jose.rfc7517.jwk import JsonWebKey
from authlib.oauth2.rfc7523 import JWTBearerToken

logger = logging.getLogger(__name__)


class KeyCloakJWTBearerTokenValidator(BearerTokenValidator):
    TOKEN_TYPE = 'bearer'
    token_cls = JWTBearerToken

    def __init__(self, issuer, realm, client_id, **extra_attributes):
        """Configure claims for Bearer Token Validator and for jwt decode.
         Retrieve public key from key cloak.

        :param domain:
        :param realm:
        """
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
        try:
            claims = jwt.decode(
                token_string, self.public_key,
                claims_options=self.claims_options,
                claims_cls=self.token_cls,
            )
            claims.validate()
            return claims
        except JoseError as error:
            logger.debug('Authenticate token failed. %r', error)
            return None
