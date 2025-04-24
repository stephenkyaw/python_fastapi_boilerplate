from src.common.mongo_repository import MongoRepository
from src.sales.domain.model import Sale


class SaleRepository(MongoRepository[Sale]):
    """Repository for managing Sale documents in MongoDB."""

    def __init__(self):
        """Initialize the SaleRepository with the given collection name."""
        super().__init__(collection_name="sales", entity_type=Sale)
