import logging
import sys
from typing import Optional


def create_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Create and configure a logger for common use across all classes and functions.

    This function creates a standardized logger instance that can be reused throughout the application.
    It provides consistent logging format and behavior across all components.
    The logger outputs to stdout and includes timestamp, log level, logger name and message.
    Handlers are only added once per logger name to avoid duplicate logging.

    Args:
        name (Optional[str]): Name of the logger, typically the module/class name.
            If None, returns the root logger.
            The name helps identify which component generated the log message.

    Returns:
        logging.Logger: A configured logger instance with:
            - DEBUG level enabled to capture all log levels
            - StreamHandler for stdout output
            - Standard format: timestamp [LEVEL] logger_name: message
            
    Example:
        In any class/function:
        >>> logger = create_logger(__name__)  # Use module name as logger name
        >>> logger.info("Processing started")
        >>> logger.error("Error occurred", exc_info=True)  # With exception details
        >>> logger.debug("Debug information")
    """
    logger = logging.getLogger(name)

    if logger.hasHandlers():
        return logger

    # Set base logging level to DEBUG to capture all levels
    logger.setLevel(logging.DEBUG)

    # Configure stream handler to write to stdout
    handler = logging.StreamHandler(sys.stdout)

    # Create formatter with standard format
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger