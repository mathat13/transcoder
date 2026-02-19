import factory

from faker import Faker

from application import (
    RootException,
)

class RetryableExceptionFactory(factory.Factory):
    class Meta:
        model = RootException
    
    retryable = True

class TerminalExceptionFactory(factory.Factory):
    class Meta:
        model = RootException

    retryable = False


