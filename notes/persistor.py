from abc import ABC, abstractmethod
from logging import getLogger
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

import attr

from .model import MODELS, Note
from .exception import NotFoundInDB


@attr.s
class DatabaseAdapter(ABC):
    logger = attr.ib(init=False, repr=False)

    def __attrs_post_init__(self):
        self.logger = getLogger(f"{__name__}.{self.__class__.__name__}")

    def save(self, obj):
        if isinstance(obj, Note):
            self.save_note(obj)
        else:
            raise ValueError("{obj} is not a supported model.")

    def filter_by(self, model_cls, **kwargs):
        if model_cls is Note:
            return self.filter_note_by(user_id=kwargs["user_id"])
        else:
            raise ValueError("{obj} is not a supported model.")

    def get(self, model_cls, **kwargs):
        if model_cls is Note:
            return self.get_note(user_id=kwargs["user_id"], note_id=kwargs["note_id"])
        else:
            raise ValueError("{obj} is not a supported model.")

    @abstractmethod
    def save_note(self, note):
        pass

    @abstractmethod
    def filter_note_by(self, user_id):
        pass


@attr.s
class NoOpAdapter(DatabaseAdapter):
    def save_note(self, note):
        pass


@attr.s
class DynamoDBAdapter(DatabaseAdapter):
    dynamodb_resource = attr.ib()
    table_name = attr.ib()
    table = attr.ib(init=False, repr=False)

    def __attrs_post_init__(self):
        self.table = self.dynamodb_resource.Table(self.table_name)

    def save_note(self, note):
        self.table.put_item(Item=note.to_json_dict())

    def filter_note_by(self, user_id):
        response = self.table.query(
            KeyConditionExpression=Key("user_id").eq(user_id)
        )
        return [Note(**item) for item in response["Items"]]

    def get_note(self, user_id, note_id):
        try:
            key = dict(user_id=user_id, note_id=note_id)
            item = self.table.get_item(Key=key).get("Item")
            return Note(**item) if item else None
        except ClientError as e:
            print(e.response["Error"]["Message"])
            return None


@attr.s
class Persistor(object):
    database_adapter = attr.ib(default=attr.Factory(NoOpAdapter))

    def save(self, obj):
        print(f"{self.database_adapter.__class__.__name__} saving {obj}")
        self.database_adapter.save(obj)

    def filter_by(self, model_cls, **kwargs):
        return self.database_adapter.filter_by(model_cls, **kwargs)

    def get(self, model_cls, **kwargs):
        return self.database_adapter.get(model_cls, **kwargs)

    def find(self, model_cls, **kwargs):
        model_cls_instance = self.database_adapter.get(model_cls, **kwargs)
        if model_cls_instance is None:
            raise NotFoundInDB(message=f"{model_cls} not found in the DB", query=kwargs)
        return model_cls_instance

