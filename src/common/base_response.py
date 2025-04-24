from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class BaseResponse:
    """Base response class for standardizing API responses.
    
    Attributes:
        status_code: HTTP status code of the response
        message: Message describing the response
        data: Optional dictionary containing response data
        
    Example:
        >>> response = BaseResponse(
        ...     status_code=200,
        ...     message="Success",
        ...     data={"user_id": 123, "username": "john_doe"}
        ... )
        >>> response.to_dict()
        {
            'status_code': 200,
            'message': 'Success', 
            'data': {
                'user_id': 123,
                'username': 'john_doe'
            }
        }
        
        >>> error_response = BaseResponse(
        ...     status_code=404,
        ...     message="User not found"
        ... )
        >>> error_response.to_dict()
        {
            'status_code': 404,
            'message': 'User not found',
            'data': {}
        }
    """
    status_code: int
    message: str 
    data: Optional[Dict[str, Any]] = None

    def __post_init__(self) -> None:
        """Initialize default values after dataclass initialization."""
        self.data = self.data or {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert the response to a dictionary format.
        
        Returns:
            Dictionary containing the response attributes
        """
        return {
            "status_code": self.status_code,
            "message": self.message,
            "data": self.data
        }
