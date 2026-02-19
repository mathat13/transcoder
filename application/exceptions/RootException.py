class RootException(Exception):
    """Base class for all exceptions."""
    retryable: bool