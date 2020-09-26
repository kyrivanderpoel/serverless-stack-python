import attr
from boto3.dynamodb.conditions import Key

from .model import Note
from ..adapter import DatabaseAdapter


@attr.s
class DynamoDBNoteAdapter(DatabaseAdapter):
    """An adapter for saving Notes in DynamoDB."""
    dynamodb_resource = attr.ib()
    table_name = attr.ib()
    table = attr.ib(init=False, repr=False)

    def __attrs_post_init__(self):
        self.table = self.dynamodb_resource.Table(self.table_name)

    def save(self, note):
        self.table.put_item(Item=note.to_json_dict())

    def filter(self, user_id):
        response = self.table.query(
            KeyConditionExpression=Key("user_id").eq(user_id)
        )
        return [Note(**item) for item in response["Items"]]

    def get(self, user_id, note_id):
        try:
            key = dict(user_id=user_id, note_id=note_id)
            item = self.table.get_item(Key=key).get("Item")
            return Note(**item) if item else None
        except ClientError as e:
            print(e.response["Error"]["Message"])
            return None

    def update(self, note, attachment, content):
        note.attachment = attachment
        note.content = content
        note.record_modification()
        self.save(note)
        return note

    def all(self):
        raise NotImplemented
