from domain import OperationContext

class FakeJellyfinAPIAdapter:
    def __init__(self):
        self.rescan_library_call_count = 0

    def rescan_library(self, context: OperationContext):
        self.rescan_library_call_count += 1