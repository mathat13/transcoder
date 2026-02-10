from domain import OperationContext

from application import JellyfinLibraryRefreshCapable

class FakeJellyfinAPIAdapter(JellyfinLibraryRefreshCapable):
    def __init__(self):
        self.refresh_library_call_count = 0

    def refresh_library(self, context: OperationContext):
        self.refresh_library_call_count += 1