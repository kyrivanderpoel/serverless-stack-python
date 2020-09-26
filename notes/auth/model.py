import attr


@attr.s
class User(object):
    user_id = attr.ib()
    password = attr.ib(repr=False, default="redacted")

    def to_dict(self):
        return dict(
            user_id=self.user_id,
        )

    def to_json_dict(self):
        return self.to_dict()
