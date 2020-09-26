import attr


@attr.s
class User(object):
    user_id = attr.ib()
    is_confirmed = attr.ib(default=False)
    password = attr.ib(repr=False, default="redacted")

    def to_dict(self):
        return dict(
            user_id=self.user_id,
            is_confirmed=self.is_confirmed,
        )

    def to_json_dict(self):
        return self.to_dict()
