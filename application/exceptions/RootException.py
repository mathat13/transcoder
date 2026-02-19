class RootException(Exception):
    """Base class for all exceptions."""
    retryable: bool

    def __init__(self, retryable: bool):
        self.retryable = retryable
        
