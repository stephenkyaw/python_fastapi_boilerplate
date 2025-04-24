class Message:
    """Common messages used in API responses.
    
    This class contains standardized messages for common API response scenarios.
    The messages are used to provide consistent communication across the API.
    
    Example:
        >>> response = BaseResponse(
        ...     status_code=200,
        ...     message=Message.SUCCESS,
        ...     data={"user": user}
        ... )
    """
    # Success messages
    SUCCESS = "The operation was successful."
    CREATED = "The resource has been created successfully."
    UPDATED = "The resource has been updated successfully."
    DELETED = "The resource has been deleted successfully."
    
    # Client error messages
    NOT_FOUND = "The requested resource could not be found."
    BAD_REQUEST = "The request contains invalid data."
    UNAUTHORIZED = "You are not authorized to perform this action."
    FORBIDDEN = "You do not have permission to access this resource."
    VALIDATION_ERROR = "There was an error validating the input data."
    
    # Server error messages
    SERVER_ERROR = "A server error occurred. Please try again later."