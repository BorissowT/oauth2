import functools

from authlib.integrations.flask_oauth2.requests import FlaskJsonRequest
from authlib.oauth2 import OAuth2Error
from authlib.oauth2.rfc6749 import TokenValidator, MissingAuthorizationError
from authlib.integrations.flask_oauth2 import ResourceProtector as RPBase, \
    token_authenticated
from flask import request as _req, g


class ResourceProtector(RPBase):
    """A protecting method for resource servers. Creating a ``require_oauth``
    decorator easily with ResourceProtector::

        require_oauth = ResourceProtector()

        # add bearer token validator

        class MyBearerTokenValidator(BearerTokenValidator):
            def authenticate_token(self, token_string):
                return Token.query.filter_by(access_token=token_string).first()

        require_oauth.register_token_validator(MyBearerTokenValidator())

        TODO rewrite usage here
        # protect resource with require_oauth

        @app.route('/user')
        @require_oauth(['profile'])
        def user_profile():
            user = User.query.get(current_token.user_id)
            return jsonify(user.to_dict())
        """

    def __call__(self, resource: str = None,
                 scopes: list[str] = None,
                 optional=None):
        def wrapper(f):
            @functools.wraps(f)
            def decorated(*args, **kwargs):
                try:
                    self.acquire_token(scopes=scopes, resource=resource)
                except MissingAuthorizationError as error:
                    if optional:
                        return f(*args, **kwargs)
                    self.raise_error_response(error)
                except OAuth2Error as error:
                    self.raise_error_response(error)
                return f(*args, **kwargs)
            return decorated
        return wrapper

    def acquire_token(self, resource: str = None, scopes: list[str] = None):
        """A method to acquire current valid token with the given scope.

        :param resource: a string name of resource in auth server
        :param scopes: a list of scope values
        :return: token object
        """
        request = FlaskJsonRequest(_req)
        # backward compatible
        if isinstance(scopes, str):
            scopes = [scopes]
        token = self.validate_request(request,
                                      scopes=scopes,
                                      resource=resource)
        token_authenticated.send(self, token=token)
        g.authlib_server_oauth2_token = token
        return token

    def validate_request(self,
                         request,
                         resource: str = None,
                         scopes: list[str] = None):
        """Validate the request and return a token."""
        validator, token_string = self.parse_request_authorization(request)
        validator.validate_request(request)
        access_token = validator.authenticate_token(token_string)
        validator.validate_token(request=request,
                                 access_token=access_token,
                                 scopes=scopes,
                                 resource=resource,
                                 access_token_string=token_string)
        return access_token
