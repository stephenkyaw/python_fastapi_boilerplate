from typing import TypeVar, List, Optional, Any, Dict, Type
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId

from .base_repository import BaseRepository
from .mongo_database import MongoDatabase

T = TypeVar('T')


class MongoRepository(T):
    """MongoDB implementation of the BaseRepository interface.
    
    Provides CRUD operations for MongoDB collections.
    
    Attributes:
        collection_name (str): Name of the MongoDB collection
        entity_type (Type[T]): The type of entity this repository handles
        mongo_database (MongoDatabase): MongoDB database connection manager
        collection (AsyncIOMotorCollection): MongoDB collection instance
    """

    def __init__(self, collection_name: str, entity_type: Type[T]) -> None:
        """Initialize the MongoDB repository.

        Args:
            collection_name: Name of the MongoDB collection
            entity_type: The type of entity this repository handles
        """
        self.collection_name = collection_name
        self.entity_type = entity_type
        self.mongo_database = MongoDatabase()
        self.collection: AsyncIOMotorCollection = self.mongo_database.get_collection(collection_name)

    def _convert_to_entity(self, document: Dict[str, Any]) -> T:
        """Convert a MongoDB document to an entity.

        Args:
            document: MongoDB document

        Returns:
            Entity instance of type T
        """
        if document and '_id' in document:
            document['id'] = str(document.pop('_id'))
        return self.entity_type(**document)

    def _convert_to_document(self, entity: T) -> Dict[str, Any]:
        """Convert an entity to a MongoDB document.

        Args:
            entity: Entity instance

        Returns:
            Dict containing the MongoDB document representation
        """
        document = entity.dict()
        if 'id' in document:
            document['_id'] = ObjectId(document.pop('id'))
        return document

    async def insert(self, entity: T) -> T:
        """Insert a single entity into the collection.

        Args:
            entity: Entity to insert

        Returns:
            The inserted entity with populated id
        """
        document = self._convert_to_document(entity)
        result = await self.collection.insert_one(document)
        entity.id = str(result.inserted_id)
        return entity

    async def insert_many(self, entities: List[T]) -> List[T]:
        """Insert multiple entities into the collection.

        Args:
            entities: List of entities to insert

        Returns:
            List of inserted entities with populated ids
        """
        documents = [self._convert_to_document(entity) for entity in entities]
        result = await self.collection.insert_many(documents)
        
        for entity, inserted_id in zip(entities, result.inserted_ids):
            entity.id = str(inserted_id)
        return entities

    async def update(self, entity: T) -> T:
        """Update a single entity in the collection.

        Args:
            entity: Entity to update

        Returns:
            The updated entity
        """
        document = self._convert_to_document(entity)
        await self.collection.replace_one({'_id': document['_id']}, document)
        return entity

    async def update_many(self, entities: List[T]) -> List[T]:
        """Update multiple entities in the collection.

        Args:
            entities: List of entities to update

        Returns:
            List of updated entities
        """
        for entity in entities:
            await self.update(entity)
        return entities

    async def delete(self, entity: T) -> None:
        """Delete a single entity from the collection.

        Args:
            entity: Entity to delete
        """
        await self.collection.delete_one({'_id': ObjectId(entity.id)})

    async def delete_many(self, entities: List[T]) -> None:
        """Delete multiple entities from the collection.

        Args:
            entities: List of entities to delete
        """
        ids = [ObjectId(entity.id) for entity in entities]
        await self.collection.delete_many({'_id': {'$in': ids}})

    async def soft_delete(self, entity: T) -> None:
        """Soft delete a single entity by setting deleted flag.

        Args:
            entity: Entity to soft delete
        """
        await self.collection.update_one(
            {'_id': ObjectId(entity.id)},
            {'$set': {'deleted': True}}
        )

    async def soft_delete_many(self, entities: List[T]) -> None:
        """Soft delete multiple entities by setting deleted flag.

        Args:
            entities: List of entities to soft delete
        """
        ids = [ObjectId(entity.id) for entity in entities]
        await self.collection.update_many(
            {'_id': {'$in': ids}},
            {'$set': {'deleted': True}}
        )

    async def find_by_id(self, id: str) -> Optional[T]:
        """Find an entity by its ID.

        Args:
            id: Entity ID to search for

        Returns:
            Found entity or None if not found
        """
        document = await self.collection.find_one({'_id': ObjectId(id)})
        return self._convert_to_entity(document) if document else None

    async def find_all(self) -> List[T]:
        """Find all entities in the collection.

        Returns:
            List of all entities
        """
        cursor = self.collection.find()
        documents = await cursor.to_list(length=None)
        return [self._convert_to_entity(doc) for doc in documents]

    async def find_by(self, **kwargs: Any) -> List[T]:
        """Find entities by query parameters.

        Args:
            **kwargs: Query parameters

        Returns:
            List of entities matching the query
        """
        if 'id' in kwargs:
            kwargs['_id'] = ObjectId(kwargs.pop('id'))
        
        cursor = self.collection.find(kwargs)
        documents = await cursor.to_list(length=None)
        return [self._convert_to_entity(doc) for doc in documents]
