from logging import getLogger
from contextlib import contextmanager
import attr
import requests

logger = getLogger(__name__)

@attr.s
class AuthClient(object):
    session = attr.ib(default=attr.Factory(requests.Session))
    endpoint = attr.ib(default="http://localhost:5000/v1/auth")

    def login(self, email, password):
        endpoint = self.endpoint + "/login"
        return self.session.post(endpoint, json=dict(user_id=email, password=password))

    def create_user(self, email, password):
        endpoint = self.endpoint + "/user"
        return self.session.post(endpoint, json=dict(user_id=email, password=password))

    def confirm(self, email):
        endpoint = self.endpoint + "/user/{email}/confirm"
        return self.session.post(endpoint)

    def logout(self, email):
        endpoint = self.endpoint + "/logout"
        return self.session.post(endpoint, json=dict(user_id=email))

    def list_users(self):
        endpoint = self.endpoint + "/user"
        return self.session.get(endpoint)

    def get_user(self, email):
        endpoint = self.endpoint + "/user/{email}"
        return self.session.get(endpoint)

    @contextmanager
    def authenticated_session(self, email, password):
        self.login(email, password)
        logger.info(f"User logged in {email}")
        yield self.session
        logger.info(f"User logged out {email}")
        self.logout(email)



