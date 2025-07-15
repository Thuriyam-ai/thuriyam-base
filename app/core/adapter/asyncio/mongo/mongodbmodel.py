from copy import deepcopy
import typing as t
from datetime import datetime
from pymongo import ASCENDING, DESCENDING

from jobnotification.adapter.asyncio.mongo.mongodbadapter import (
    MongoDBAsyncAdapter,
)


class ImproperMongoModelConfigError(Exception):
    """Exception raised for improper MongoDB model configuration"""
    pass


class MongoModel:
    """Base MongoDB model class"""
    adapter = None
    collection = None
    read_cursor = None
    write_cursor = None
    SERVER_TIMESTAMP_KEY = "server_timestamp"
    
    def _validate_params(self):
        """Validate model parameters"""
        if not isinstance(self.adapter, MongoDBAsyncAdapter):
            raise ImproperMongoModelConfigError(
                f"{type(self).__name__} | `adapter` is expected of type `MongoDBAsyncAdapter`, got {type(self.adapter)} instead"
            )
        return True
    
    def _validate_doc(self, content):
        """Validate document content"""
        if not isinstance(content, dict):
            raise ValueError("Content must be a dictionary")
        return True
    
    def _get_server_timestamp(self):
        """Get server timestamp"""
        return datetime.utcnow()


class MongoAsyncModel(MongoModel):
    adapter: MongoDBAsyncAdapter = None

    def _validate_params(self):
        if not isinstance(self.adapter, MongoDBAsyncAdapter):
            raise ImproperMongoModelConfigError(
                f"{type(self).__name__} | `adapter` is expected of type `MongoDBAsyncAdapter`, got {type(self.adapter)} instead"
            )
        return super()._validate_params()

    async def _set_indices(self):
        is_server_timestamp_indexed = False

        for index in self.collection.indices:
            kwargs = deepcopy(index.__dict__)

            del kwargs["keys"]
            if "background" not in kwargs:
                kwargs["background"] = True

            await self.write_cursor.create_index(index.keys, **kwargs)

            if index.keys == self.SERVER_TIMESTAMP_KEY:
                is_server_timestamp_indexed = True
            elif isinstance(index.keys, list):
                for key in index.keys:
                    if key[0] == self.SERVER_TIMESTAMP_KEY:
                        is_server_timestamp_indexed = True

        if not is_server_timestamp_indexed:
            await self.write_cursor.create_index(
                self.SERVER_TIMESTAMP_KEY, background=True
            )

    async def save(self, content: t.Dict[str, t.Any]):
        """
        Insert or update a single document

         - content : The document to be save

         Note: If the collection has defined a `save_filter`, then all keys required by the `save_filter`
         must be present in content
        """
        self._validate_doc(content)
        if self.SERVER_TIMESTAMP_KEY not in content:
            content[self.SERVER_TIMESTAMP_KEY] = self._get_server_timestamp()

        if self.collection.save_filter:
            _filter = self.collection.get_save_filter(content)
            cursor = await self.write_cursor.find_one(_filter)

            if cursor:
                # Document exists | Update document
                await self.update(_filter, content)
            else:
                await self.write_cursor.insert_one(content)
        else:
            await self.write_cursor.insert_one(content)

        await self._set_indices()

    async def update(self, filter_params, data):
        """
        Update one document at a time
        """
        await self.write_cursor.update_one(filter_params, {"$set": data})

    async def update_many(self, filter_params, data):
        """
        Update all documents which match filter_params
        """
        await self.write_cursor.update_many(filter_params, {"$set": data})

    async def filter(self, **kwargs):
        """
        Filter mongo documents

        Defined keyword args used for operation:
        - limit : Limit number of documents returned from query result
        - offset : Skip the first `offset` results from query result
        - sort : List of (key, direction) pairs specifying the keys to sort on.
                    Eg. [('field1', pymongo.ASCENDING), ('field2', pymongo.DESCENDING)]
        - exclude_fields : List of `strings` to be removed from filter output
        """

        _limit = 10
        _offset = 0
        _sort = []
        _exclude_fields = []

        if "limit" in kwargs:
            _limit = kwargs.pop("limit")

        if "offset" in kwargs:
            _offset = kwargs.pop("offset")

        if "sort" in kwargs:
            _sort = kwargs.pop("sort")

        if "exclude_fields" in kwargs:
            _exclude_fields = kwargs.pop("exclude_fields")

        cursor = self.read_cursor.find(kwargs).limit(_limit).skip(_offset)

        if _sort:
            cursor = cursor.sort(_sort)
        documents = await cursor.to_list(length=_limit)
        data = []

        for c in documents:
            c.pop("_id", None)
            if _exclude_fields:
                for field in _exclude_fields:
                    c.pop(field, None)
            data.append(c)

        return data

    async def count(self, **kwargs):
        """
        Count filtered documents
        """
        count = await self.read_cursor.count_documents(kwargs)
        return count

    async def delete_one(self, **kwargs):
        """
        Delete single document
        """
        return await self.write_cursor.delete_one(kwargs)

    async def delete_many(self, **kwargs):
        """
        Delete multiple documents
        """
        return await self.write_cursor.delete_many(kwargs)

    async def get_document_by_id(self, _id: str):
        """
        Get single document by id
        """
        filter_param = {"_id": _id}
        doc = await self.read_cursor.find_one(filter_param)
        return doc
