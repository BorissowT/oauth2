"""Python Flask API Auth0 integration example
"""

from flask import Flask, jsonify
from authlib.integrations.flask_oauth2 import ResourceProtector
from validator import KeyCloakJWTBearerTokenValidator
from flask_cors import CORS


require_auth = ResourceProtector()
validator = KeyCloakJWTBearerTokenValidator(
    # Here is the problem with mapping of localhost to my local network ip.
    "http://192.168.105.139:8080/auth/realms/myrealm",
    "myrealm",
    "myapi"
)
require_auth.register_token_validator(validator)

APP = Flask(__name__)
cors = CORS(APP, supports_credentials=True)


@APP.route("/api/public")
def public():
    """No access token required."""
    response = (
        "Hello from a public endpoint! You don't need to be"
        " authenticated to see this."
    )
    return jsonify(message=response)


@APP.route("/api/private")
@require_auth(None)
def private():
    """A valid access token is required."""
    response = (
        "PRIVet!"
    )
    return jsonify(message=response)


@APP.route("/api/messages")
@require_auth("read:messages")
def read_messages():
    """A valid access token and scope are required."""
    response = (
        "Hello from a private endpoint! read:messages"
    )
    return jsonify(message=response)


@APP.route("/api/messages", methods=['POST'])
@require_auth("write:messages")
def write_messages():
    """A valid access token and scope are required."""
    response = (
        "Hello from a private endpoint! write:messages"
    )
    return jsonify(message=response)


if __name__ == '__main__':
    APP.run(host="0.0.0.0", port=5005)
