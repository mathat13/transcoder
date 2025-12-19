from datetime import datetime, timezone
from dataclasses import dataclass, field
from uuid import UUID

@dataclass(kw_only=True)
class Event:
    """Marker base class for all events."""
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))