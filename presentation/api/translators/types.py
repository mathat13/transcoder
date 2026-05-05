from enum import Enum

class IgnoreReason(str, Enum):
    UNSUPPORTED_EVENT_TYPE = "unsupported_event_type"
