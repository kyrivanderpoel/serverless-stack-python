from datetime import datetime
import uuid

import attr

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
    modified_date = attr.ib(converter=iso_string_to_datetime, default=attr.Factory(datetime.utcnow))
    # Use a randomly generated GUID for the default note_id.
    note_id = attr.ib()

    def to_dict(self):
        return attr.asdict(self)

    def to_json_dict(self):
        d = self.to_dict()
        d["created_date"] = self.created_date.isoformat()
        d["modified_date"] = self.modified_date.isoformat()
        return d

    def record_modification(self):
        self.modified_date = datetime.utcnow()

    @note_id.default
    def _guid_string(self):
        return str(uuid.uuid4())
