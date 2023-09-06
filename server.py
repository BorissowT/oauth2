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
    issuer="http://192.168.105.139:8080/auth/realms/myrealm",
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


@APP.route("/api/rooms", methods=['GET'])
@require_auth(resource='rooms', scopes=["read"])
def get_rooms():
    """A valid access token is required."""
    response = (
        "<<<<<<<ROOMS GET>>>>>>>"
    )
    return jsonify(message=response)


@APP.route("/api/rooms", methods=['POST'])
@require_auth(resource='rooms', scopes=["write"])
def create_rooms():
    """A valid access token is required."""
    response = (
        "<<<<<<<ROOMS POST>>>>>>>"
    )
    return jsonify(message=response)


@APP.route("/api/rooms", methods=['PUT'])
@require_auth(resource='rooms', scopes=["update"])
def update_rooms():
    """A valid access token is required."""
    response = (
        "<<<<<<<ROOMS PUT>>>>>>>"
    )
    return jsonify(message=response)


@APP.route("/api/rooms", methods=['DELETE'])
@require_auth(resource='rooms', scopes=["delete"])
def delete_rooms():
    """A valid access token is required."""
    response = (
        "<<<<<<<ROOMS DELETE>>>>>>>"
    )
    return jsonify(message=response)


@APP.route("/api/apartments", methods=['GET'])
@require_auth(resource='apartments', scopes=["read"])
def get_apartments():
    """A valid access token is required."""
    response = (
        "<<<<<<<APARTMENTS GET>>>>>>>"
    )
    return jsonify(message=response)


@APP.route("/api/apartments", methods=['POST'])
@require_auth(resource='apartments', scopes=["write"])
def create_apartments():
    """A valid access token is required."""
    response = (
        "<<<<<<<APARTMENTS POST>>>>>>>"
    )
    return jsonify(message=response)


@APP.route("/api/apartments", methods=['PUT'])
@require_auth(resource='apartments', scopes=["update"])
def update_apartments():
    """A valid access token is required."""
    response = (
        "<<<<<<<APARTMENTS PUT>>>>>>>"
    )
    return jsonify(message=response)


@APP.route("/api/apartments", methods=['DELETE'])
@require_auth(resource='apartments', scopes=["delete"])
def delete_apartments():
    """A valid access token is required."""
    response = (
        "<<<<<<<APARTMENTS DELETE>>>>>>>"
    )
    return jsonify(message=response)


if __name__ == '__main__':
    APP.run(host="0.0.0.0", port=5005)
