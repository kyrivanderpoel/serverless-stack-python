import uuid
import attr
from datetime import datetime

def iso_string_to_datetime(obj):
    if isinstance(obj, datetime):
        return obj
    else:
        return datetime.fromisoformat(obj)

@attr.s
class Note(object):
    user_id = attr.ib()
    content = attr.ib()
    attachment = attr.ib()
    # Use right now as the default created_date.
    created_date = attr.ib(converter=iso_string_to_datetime, default=attr.Factory(datetime.utcnow))
    # Use a randomly generated GUID for the default note_id.
    note_id = attr.ib()

    def to_dict(self):
        return dict(
            user_id=self.user_id,
            content=self.content,
            attachment=self.attachment,
            created_date=self.created_date,
            note_id=self.note_id,
        )

    def to_json_dict(self):
        d = self.to_dict()
        d["created_date"] = self.created_date.isoformat()
        return d

    @note_id.default
    def _guid_string(self):
        return str(uuid.uuid4())


MODELS = set([Note])
