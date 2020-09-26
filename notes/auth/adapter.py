from warrant import Cognito
import attr

from .model import User
from ..adapter import DatabaseAdapter
from ..exception import NotAuthenticated


@attr.s
class CognitoUserAdapter(DatabaseAdapter):
    pool_id = attr.ib()
    client_id = attr.ib()
    cognito_idp_client = attr.ib()

    def save(self, user):
        u = Cognito(self.pool_id, self.client_id)
        u.add_base_attributes(email=user.user_id)
        u.register(user.user_id, user.password)

    def get(self, user_id):
        u = Cognito(self.pool_id, self.client_id, username=user_id)
        return u.get_user()

    def filter(self, **kwargs):
        raise NotImplemented

    def all(self):
        u = Cognito(self.pool_id, self.client_id)
        users = u.get_users(attr_map={"email": "email"})
        print(users)
        print(users[0]._attr_map)
        for user in users:
            print(user.username)
        print(dir(users[0]))
        print(dir(users[1]))
        return users

    def login(self, user):
        u = Cognito(self.pool_id, self.client_id, username=user.user_id)
        u.authenticate(password=user.password)
        print(dir(u))
        attrs = ["id_token", "refresh_token", "access_token", "token_type"]

        return {attr: getattr(u, attr) for attr in attrs}

    def logout(self, auth):
        u = Cognito(
            self.pool_id,
            self.client_id,
            id_token=auth["id_token"],
            refresh_token=auth["refresh_token"],
            access_token=auth["access_token"],
        )


    def admin_confirm_signup(self, user):
        self.cognito_idp_client.admin_confirm_sign_up(
            UserPoolId=self.pool_id,
            Username=user.user_id,
        )

    def check_auth(self, auth):
        u = Cognito(
            self.pool_id,
            self.client_id,
            id_token=auth.get("id_token"),
            refresh_token=auth.get("refresh_token"),
            access_token=auth.get("access_token"),
        )
        try:
            u.check_token()
        except AttributeError:
            raise NotAuthenticated
