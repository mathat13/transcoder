import pytest
from uuid import UUID

from presentation import build_operation_context

from domain import OperationContext

def test_build_operation_context_builds_operation_context_correctly():
    ctx = build_operation_context()

    assert isinstance(ctx.operation_id, UUID)
    assert isinstance(ctx, OperationContext)
