from flask.json import JSONEncoder
from datetime import datetime


class ISOFormatJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)
