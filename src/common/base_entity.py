from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class BaseEntity:
    """Base entity class with common audit fields."""
    
    created_by: Optional[str] = field(default=None)
    created_at: datetime = field(default_factory=datetime.now)
    updated_by: Optional[str] = field(default=None)
    updated_at: Optional[datetime] = field(default=None)
    is_deleted: bool = field(default=False)
    is_active: bool = field(default=True)
