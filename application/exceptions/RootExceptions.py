class RootException(Exception):
    """Base class for all exceptions."""
    retryable: bool

class RetryableException(RootException):
    """Base retryable exception."""

class TerminalException(RootException):
    """Base non-retryable exception."""
        
