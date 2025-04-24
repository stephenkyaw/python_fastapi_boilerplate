from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Any, Dict

T = TypeVar('T')

class BaseRepository(ABC, Generic[T]):
    """
    Base repository interface defining standard CRUD operations.
    Can be implemented by MongoDB or SQLAlchemy repositories.
    """

    @abstractmethod
    async def insert(self, entity: T) -> T:
        """Insert a single entity.

        Args:
            entity: The entity to insert

        Returns:
            The inserted entity with any generated fields populated
        """
        raise NotImplementedError

    @abstractmethod
    async def insert_many(self, entities: List[T]) -> List[T]:
        """Insert multiple entities in bulk.

        Args:
            entities: List of entities to insert

        Returns:
            List of inserted entities with any generated fields populated
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, entity: T) -> T:
        """Update a single entity.

        Args:
            entity: The entity to update with new values

        Returns:
            The updated entity
        """
        raise NotImplementedError

    @abstractmethod
    async def update_many(self, entities: List[T]) -> List[T]:
        """Update multiple entities in bulk.

        Args:
            entities: List of entities to update

        Returns:
            List of updated entities
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, entity: T) -> None:
        """Hard delete a single entity.

        Args:
            entity: The entity to delete
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_many(self, entities: List[T]) -> None:
        """Hard delete multiple entities in bulk.

        Args:
            entities: List of entities to delete
        """
        raise NotImplementedError

    @abstractmethod
    async def soft_delete(self, entity: T) -> None:
        """Soft delete a single entity by marking it as deleted.

        Args:
            entity: The entity to soft delete
        """
        raise NotImplementedError

    @abstractmethod
    async def soft_delete_many(self, entities: List[T]) -> None:
        """Soft delete multiple entities in bulk by marking them as deleted.

        Args:
            entities: List of entities to soft delete
        """
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(self, id: str) -> Optional[T]:
        """Find an entity by its unique identifier.

        Args:
            id: The unique identifier of the entity

        Returns:
            The found entity or None if not found
        """
        raise NotImplementedError

    @abstractmethod
    async def find_all(self) -> List[T]:
        """Retrieve all entities.

        Returns:
            List of all entities
        """
        raise NotImplementedError

    @abstractmethod
    async def find_by(self, **kwargs: Any) -> List[T]:
        """Find entities matching the given criteria.

        Args:
            **kwargs: Filter criteria as keyword arguments

        Returns:
            List of entities matching the criteria
        """
        raise NotImplementedError