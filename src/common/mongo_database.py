from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection

from .config import AppSettings
from .logger import create_logger

logger = create_logger(__name__)


class MongoDatabase:
    """MongoDB database connection manager using Motor for async operations.
    
    This class implements the singleton pattern to maintain a single database connection
    across the application. It provides async database operations using Motor.
    
    Attributes:
        _instance (Optional[MongoDatabase]): Singleton instance of the class
        client (AsyncIOMotorClient): Motor AsyncIO MongoDB client instance
        database (AsyncIOMotorDatabase): Motor AsyncIO MongoDB database instance
        
    Example:
        >>> # Get database instance
        >>> db = MongoDatabase()
        >>> collection = db.get_collection("users")
        >>> 
        >>> # Use in async context
        >>> async def get_user(user_id: str):
        ...     return await collection.find_one({"_id": user_id})
        >>>
        >>> # Close connection when done
        >>> await db.close()
    """
    
    _instance: Optional['MongoDatabase'] = None
    
    def __new__(cls) -> 'MongoDatabase':
        """Implement singleton pattern to reuse database connection.
        
        Returns:
            MongoDatabase: Singleton instance of the database manager
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initialize MongoDB connection if not already initialized."""
        if not hasattr(self, 'client'):
            self._initialize_db()

    def _initialize_db(self) -> None:
        """Initialize MongoDB connection using Motor.
        
        Raises:
            Exception: If connection fails or environment variables are missing
        """
        try:
            mongo_uri = self._get_connection_uri()
            db_name = self._get_database_name()

            self.client: AsyncIOMotorClient = AsyncIOMotorClient(
                mongo_uri,
                serverSelectionTimeoutMS=5000  # 5 second timeout
            )
            self.database: AsyncIOMotorDatabase = self.client[db_name]

            # Test connection
            self.client.server_info()
            logger.info(f"Successfully connected to MongoDB database: {db_name}")
            
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise

    def _get_connection_uri(self) -> str:
        """Get MongoDB connection URI from environment variables.
        
        Returns:
            str: MongoDB connection URI
            
        Raises:
            ValueError: If MONGODB_URI environment variable is not set
        """
        uri = AppSettings.MONGODB_URI
        if not uri:
            error_msg = "MONGODB_URI environment variable is not set"
            logger.error(error_msg)
            raise ValueError(error_msg)
        return uri

    def _get_database_name(self) -> str:
        """Get MongoDB database name from environment variables.
        
        Returns:
            str: MongoDB database name
            
        Raises:
            ValueError: If MONGODB_DB_NAME environment variable is not set
        """
        db_name = AppSettings.MONGODB_DB_NAME
        if not db_name:
            error_msg = "MONGODB_DB_NAME environment variable is not set"
            logger.error(error_msg)
            raise ValueError(error_msg)
        return db_name

    async def close(self) -> None:
        """Close MongoDB connection safely.
        
        This method should be called when shutting down the application
        to properly close the database connection.
        """
        if hasattr(self, 'client'):
            self.client.close()
            logger.info("MongoDB connection closed")

    def get_database(self) -> AsyncIOMotorDatabase:
        """Get the database instance.
        
        Returns:
            AsyncIOMotorDatabase: Motor async MongoDB database instance
        """
        return self.database

    def get_collection(self, collection_name: str) -> AsyncIOMotorCollection:
        """Get a collection from the database.
        
        Args:
            collection_name: Name of the collection to get
            
        Returns:
            AsyncIOMotorCollection: Motor async MongoDB collection instance
            
        Example:
            >>> db = MongoDatabase()
            >>> users_collection = db.get_collection("users")
            >>> await users_collection.find_one({"email": "user@example.com"})
        """
        return self.database[collection_name]
