"""Contains an interface for performing common database operations.

We opt for this interface instead of using an ORM directly so our views are decoupled from the DB that we are using.
"""

from abc import ABC, abstractmethod
from logging import getLogger

import attr

from .exception import NotFoundInDB


@attr.s
class DatabaseAdapter(ABC):
    """A simple interface with common database operations."""
    logger = attr.ib(init=False, repr=False)

    def __attrs_post_init__(self):
        self.logger = getLogger(f"{__name__}.{self.__class__.__name__}")

    @abstractmethod
    def save(self, obj):
        pass

    @abstractmethod
    def filter(self, **kwargs):
        pass

    @abstractmethod
    def get(self, **kwargs):
        pass

    @abstractmethod
    def all(self, **kwargs):
        pass

    def find(self, **kwargs):
        instance = self.get(**kwargs)
        if instance is None:
            raise NotFoundInDB(message=f"Not found in the DB", query=kwargs)
        return instance


@attr.s
class NoOpAdapter(DatabaseAdapter):
    def save(self, obj):
        pass

    def filter(self):
        pass

    def get(self, obj):
        pass

    def all(self):
        pass
