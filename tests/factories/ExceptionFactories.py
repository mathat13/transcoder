import factory

from faker import Faker

from application import (
    RetryableException,
    TerminalException,
)

class RetryableExceptionFactory(factory.Factory):
    class Meta:
        model = RetryableException

class TerminalExceptionFactory(factory.Factory):
    class Meta:
        model = TerminalException


