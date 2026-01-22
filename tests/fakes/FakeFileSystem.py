from collections import Counter

class FakeFileSystem:
    def __init__(self):
        self._files: dict[str, int] = {}
        self._dirs: dict[str, int] = {}
        self._link_count = Counter()
        self._next_inode = 1

    def _exists(self, path: str) -> bool:
        return path in self._files or path in self._dirs

    def is_file(self, path: str) -> bool:
        return path in self._files

    def _is_dir(self, path: str) -> bool:
        return path in self._dirs
    
    def _inode(self, path: str) -> int:
        inode, _ = self._inode_for(path)
        return inode
    
    def _inode_for(self, path: str) -> tuple[int, bool]:
        if self.is_file(path):
            return self._files[path], False
        if self._is_dir(path):
            return self._dirs[path], True
        raise FileNotFoundError(path)
    
    def add(self, path: str, is_dir: bool = False) -> None:
        if self._exists(path):
            raise FileExistsError(path)

        inode = self._next_inode
        self._next_inode += 1

        if is_dir:
            self._dirs[path] = inode
        else:
            self._files[path] = inode

        self._link_count[inode] += 1

    def hardlink(self, source: str, dest: str) -> None:
        inode, is_dir = self._inode_for(source)

        if is_dir:
            raise IsADirectoryError(source)
        
        if self._is_dir(dest):
            raise NotImplementedError(dest)

        if self._exists(dest):
            raise FileExistsError(dest)

        self._files[dest] = inode
        self._link_count[inode] += 1

    def delete(self, path: str) -> None:
        inode, is_dir = self._inode_for(path)

        if is_dir:
            del self._dirs[path]
        elif self.is_file(path):
            del self._files[path]
        else:
            raise FileNotFoundError(path)

        self._link_count[inode] -= 1
        if self._link_count[inode] == 0:
            del self._link_count[inode]
