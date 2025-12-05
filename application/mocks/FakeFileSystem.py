
class FakeFileSystem:

    def exists(self, path: str) -> bool:
        return bool(path)

