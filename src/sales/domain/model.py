from uuid import uuid4
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional

from src.common.base_entity import BaseEntity


@dataclass
class SaleItem(BaseEntity):
    """
    Sale item model representing an individual item in a sale.
    
    Attributes:
        id: Unique identifier for the sale item
        sale_id: Reference to the parent sale
        product_id: Reference to the product
        quantity: Number of items sold
        price: Unit price of the item
        total_amount: Total amount for this line item (quantity * price)
    """
    id: str = field(default_factory=lambda: str(uuid4()))
    sale_id: Optional[str] = field(default=None)
    product_id: Optional[str] = field(default=None)
    quantity: int = field(default=0)
    price: float = field(default=0.0)
    total_amount: float = field(default=0.0)


@dataclass
class Sale(BaseEntity):
    """
    Sale model representing a complete sales transaction.
    
    Attributes:
        id: Unique identifier for the sale
        invoice_number: Reference number for the sale
        sale_date: Date and time when the sale occurred
        customer_id: Reference to the customer
        total_amount: Total amount of the sale
        total_items: Total number of items in the sale
    """
    id: str = field(default_factory=lambda: str(uuid4()))
    invoice_number: Optional[str] = field(default=None)
    sale_date: datetime = field(default_factory=datetime.now)
    customer_id: Optional[str] = field(default=None)
    total_amount: float = field(default=0.0)
    total_items: int = field(default=0)

