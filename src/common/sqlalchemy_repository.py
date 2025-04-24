from typing import TypeVar, List, Optional, Any, Type
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from .base_repository import BaseRepository
from .sql_database import SQLDatabase, Base

T = TypeVar('T', bound=Base)

class SQLAlchemyRepository(BaseRepository[T]):
    """SQLAlchemy implementation of the BaseRepository interface.
    
    Provides CRUD operations for SQLAlchemy models.
    
    Attributes:
        model_type (Type[T]): The SQLAlchemy model type this repository handles
        db (SQLDatabase): SQL database connection manager
    """

    def __init__(self, model_type: Type[T]) -> None:
        """Initialize the SQLAlchemy repository.

        Args:
            model_type: The SQLAlchemy model type this repository handles
        """
        self.model_type = model_type
        self.db = SQLDatabase()

    async def insert(self, entity: T) -> T:
        """Insert a single entity into the database.

        Args:
            entity: Entity to insert

        Returns:
            The inserted entity
        """
        async with self.db.get_session() as session:
            session.add(entity)
            await session.commit()
            await session.refresh(entity)
            return entity

    async def insert_many(self, entities: List[T]) -> List[T]:
        """Insert multiple entities into the database.

        Args:
            entities: List of entities to insert

        Returns:
            List of inserted entities
        """
        async with self.db.get_session() as session:
            for entity in entities:
                session.add(entity)
            await session.commit()
            for entity in entities:
                await session.refresh(entity)
            return entities

    async def update(self, entity: T) -> T:
        """Update a single entity in the database.

        Args:
            entity: Entity to update

        Returns:
            The updated entity
        """
        async with self.db.get_session() as session:
            await session.merge(entity)
            await session.commit()
            await session.refresh(entity)
            return entity

    async def update_many(self, entities: List[T]) -> List[T]:
        """Update multiple entities in the database.

        Args:
            entities: List of entities to update

        Returns:
            List of updated entities
        """
        async with self.db.get_session() as session:
            for entity in entities:
                await session.merge(entity)
            await session.commit()
            for entity in entities:
                await session.refresh(entity)
            return entities

    async def delete(self, entity: T) -> None:
        """Delete a single entity from the database.

        Args:
            entity: Entity to delete
        """
        async with self.db.get_session() as session:
            await session.delete(entity)
            await session.commit()

    async def delete_many(self, entities: List[T]) -> None:
        """Delete multiple entities from the database.

        Args:
            entities: List of entities to delete
        """
        async with self.db.get_session() as session:
            for entity in entities:
                await session.delete(entity)
            await session.commit()

    async def soft_delete(self, entity: T) -> None:
        """Soft delete a single entity by setting deleted flag.

        Args:
            entity: Entity to soft delete
        """
        async with self.db.get_session() as session:
            stmt = (
                update(self.model_type)
                .where(self.model_type.id == entity.id)
                .values(deleted=True)
            )
            await session.execute(stmt)
            await session.commit()

    async def soft_delete_many(self, entities: List[T]) -> None:
        """Soft delete multiple entities by setting deleted flag.

        Args:
            entities: List of entities to soft delete
        """
        async with self.db.get_session() as session:
            ids = [entity.id for entity in entities]
            stmt = (
                update(self.model_type)
                .where(self.model_type.id.in_(ids))
                .values(deleted=True)
            )
            await session.execute(stmt)
            await session.commit()

    async def find_by_id(self, id: str) -> Optional[T]:
        """Find an entity by its ID.

        Args:
            id: Entity ID to search for

        Returns:
            Found entity or None if not found
        """
        async with self.db.get_session() as session:
            stmt = select(self.model_type).where(self.model_type.id == id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def find_all(self) -> List[T]:
        """Find all entities in the database.

        Returns:
            List of all entities
        """
        async with self.db.get_session() as session:
            stmt = select(self.model_type)
            result = await session.execute(stmt)
            return list(result.scalars().all())

    async def find_by(self, **kwargs: Any) -> List[T]:
        """Find entities by query parameters.

        Args:
            **kwargs: Query parameters

        Returns:
            List of entities matching the query
        """
        async with self.db.get_session() as session:
            stmt = select(self.model_type)
            for key, value in kwargs.items():
                stmt = stmt.where(getattr(self.model_type, key) == value)
            result = await session.execute(stmt)
            return list(result.scalars().all())

    async def find_by_with_relations(self, relations: List[str], **kwargs: Any) -> List[T]:
        """Find entities by query parameters with related entities loaded.

        Args:
            relations: List of relation names to load
            **kwargs: Query parameters

        Returns:
            List of entities matching the query with relations loaded
        """
        async with self.db.get_session() as session:
            stmt = select(self.model_type)
            for relation in relations:
                stmt = stmt.options(selectinload(getattr(self.model_type, relation)))
            for key, value in kwargs.items():
                stmt = stmt.where(getattr(self.model_type, key) == value)
            result = await session.execute(stmt)
            return list(result.scalars().all())