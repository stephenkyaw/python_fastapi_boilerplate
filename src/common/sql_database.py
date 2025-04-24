from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from .config import AppSettings
from .logger import create_logger

logger = create_logger(__name__)

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass

class SQLDatabase:
    """SQL database connection manager using SQLAlchemy for async operations.
    
    This class implements the singleton pattern to maintain a single database connection
    across the application. It provides async database operations using SQLAlchemy.
    
    Attributes:
        _instance (Optional[SQLDatabase]): Singleton instance of the class
        engine: SQLAlchemy async engine instance
        session_factory: SQLAlchemy async session factory
    """
    
    _instance: Optional['SQLDatabase'] = None
    
    def __new__(cls) -> 'SQLDatabase':
        """Implement singleton pattern to reuse database connection.
        
        Returns:
            SQLDatabase: Singleton instance of the database manager
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initialize SQL database connection if not already initialized."""
        if not hasattr(self, 'engine'):
            self._initialize_db()

    def _initialize_db(self) -> None:
        """Initialize SQL database connection using SQLAlchemy.
        
        Raises:
            Exception: If connection fails or environment variables are missing
        """
        try:
            # Get database configuration from settings
            db_url = self._get_connection_url()
            
            # Create async engine
            self.engine = create_async_engine(
                db_url,
                echo=AppSettings.SQL_ECHO,
                pool_size=AppSettings.SQL_POOL_SIZE,
                max_overflow=AppSettings.SQL_MAX_OVERFLOW,
                pool_timeout=AppSettings.SQL_POOL_TIMEOUT,
                pool_recycle=AppSettings.SQL_POOL_RECYCLE,
            )
            
            # Create session factory
            self.session_factory = async_sessionmaker(
                self.engine,
                class_=AsyncSession,
                expire_on_commit=False,
                autocommit=False,
                autoflush=False,
            )
            
            logger.info("Successfully connected to SQL database")
            
        except Exception as e:
            logger.error(f"Failed to connect to SQL database: {str(e)}")
            raise

    def _get_connection_url(self) -> str:
        """Get SQL database connection URL from environment variables.
        
        Returns:
            str: SQL database connection URL
            
        Raises:
            ValueError: If SQL_DATABASE_URL environment variable is not set
        """
        db_url = AppSettings.SQL_DATABASE_URL
        if not db_url:
            error_msg = "SQL_DATABASE_URL environment variable is not set"
            logger.error(error_msg)
            raise ValueError(error_msg)
        return db_url

    async def get_session(self) -> AsyncSession:
        """Get a new database session.
        
        Returns:
            AsyncSession: SQLAlchemy async session
            
        Example:
            >>> db = SQLDatabase()
            >>> async with db.get_session() as session:
            ...     result = await session.execute(select(User))
            ...     users = result.scalars().all()
        """
        return self.session_factory()

    async def close(self) -> None:
        """Close SQL database connection safely.
        
        This method should be called when shutting down the application
        to properly close the database connection.
        """
        if hasattr(self, 'engine'):
            await self.engine.dispose()
            logger.info("SQL database connection closed")

    def get_base(self) -> type[Base]:
        """Get the SQLAlchemy declarative base.
        
        Returns:
            type[Base]: SQLAlchemy declarative base class
        """
        return Base
