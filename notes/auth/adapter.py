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
        response = self.cognito_idp_client.admin_get_user(
            UserPoolId=self.pool_id,
            Username=user_id
        )

        is_confirmed = True if response["UserStatus"] == "CONFIRMED" else False
        email = None
        for attr_d in response["UserAttributes"]:
            if attr_d["Name"] == "email":
                email = attr_d["Value"]
        return User(user_id=email, is_confirmed=is_confirmed)

    def filter(self, **kwargs):
        raise NotImplemented

    def all(self):
        response = self.cognito_idp_client.list_users(
            UserPoolId=self.pool_id,
            AttributesToGet=["email", "email_verified"],
        )
        users = []
        for user in response["Users"]:
            email = None
            is_confirmed = True if user["UserStatus"] == "CONFIRMED" else False
            for attr_d in user["Attributes"]:
                if attr_d["Name"] == "email":
                    email = attr_d["Value"]
            users.append(User(user_id=email, is_confirmed=is_confirmed))
        return users

    def login(self, user):
        u = Cognito(self.pool_id, self.client_id, username=user.user_id)
        u.authenticate(password=user.password)
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

        u.logout()


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
