import json
from urllib.request import urlopen

from authlib.oauth2.rfc7523 import JWTBearerTokenValidator
from authlib.jose.rfc7517.jwk import JsonWebKey


class KeyCloakJWTBearerTokenValidator(JWTBearerTokenValidator):
    def __init__(self, domain, audience, realm):
        """Retrieve public key from key cloak.

        :param domain:
        :param realm:
        :param audience:
        """
        issuer = f"https://{domain}/"
        jsonurl = urlopen(f"http://{domain}/auth/realms/"
                          f"{realm}/protocol/openid-connect/certs")
        public_key = JsonWebKey.import_key_set(
            json.loads(jsonurl.read())
        )
        super(KeyCloakJWTBearerTokenValidator, self).__init__(
            public_key
        )
        self.claims_options = {
            "exp": {"essential": True},
            "aud": {"essential": True, "value": audience},
            "iss": {"essential": True, "value": issuer},
        }
