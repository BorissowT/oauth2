"""Python Flask API Auth0 integration example
"""

from flask import Flask, jsonify, request

from resource_protector import ResourceProtector
from validator import KeyCloakJWTBearerTokenValidator
from flask_cors import CORS


require_auth = ResourceProtector()
validator = KeyCloakJWTBearerTokenValidator(
    # Here is the problem with mapping of localhost to my local network ip.
    #"http://192.168.105.139:8080/realms/myrealm",
    issuer="http://localhost:8080/auth/realms/myrealm",
    realm="myrealm",
    client_id="myclient"
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


@APP.route("/api/buildings")
@require_auth(None)
def private():
    """A valid access token is required."""
    response = (
        "HELLO FROM A PRIVATE ENDPOINT"
    )
    return jsonify(message=response)


@APP.route("/api/messages", methods=['GET'])
@require_auth(resource='message', scopes=["read"])
def read_messages():
    """A valid access token and scope are required."""
    response = (
        "GET"
    )
    return jsonify(message=response)


@APP.route("/api/messages", methods=['POST'])
@require_auth(resource='message', scopes=["write"])
def write_messages():
    """A valid access token and scope are required."""
    response = (
        "POST"
    )
    return jsonify(message=response)


if __name__ == '__main__':
    APP.run(host="0.0.0.0", port=5005)
