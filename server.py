"""Python Flask API Auth0 integration example
"""

from flask import Flask, jsonify
from authlib.integrations.flask_oauth2 import ResourceProtector
from validator import KeyCloakJWTBearerTokenValidator

require_auth = ResourceProtector()
validator = KeyCloakJWTBearerTokenValidator(
    "localhost:8080",
    "myapi",
    "myrealm"
)
require_auth.register_token_validator(validator)

APP = Flask(__name__)


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
        "Hello from a private endpoint! You need to be"
        " authenticated to see this."
    )
    return jsonify(message=response)


@APP.route("/api/private-scoped")
@require_auth("read:messages")
def private_scoped():
    """A valid access token and scope are required."""
    response = (
        "Hello from a private endpoint! You need to be"
        " authenticated and have a scope of read:messages to see"
        " this."
    )
    return jsonify(message=response)


if __name__ == '__main__':
    APP.run(debug=True)
