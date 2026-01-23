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
        inode = self._inode_for(path)
        return inode
    
    def _inode_for(self, path: str) -> int:
        if self.is_file(path):
            return self._files[path]
        if self._is_dir(path):
            return self._dirs[path]
        raise FileNotFoundError(path)
    
    def add(self, path: str, is_dir: bool = False) -> None:
        """
        Helper for instantiating filesystem.
        """
        if self._exists(path):
            raise FileExistsError(path)

        inode = self._next_inode
        self._next_inode += 1

        if is_dir:
            self._dirs[path] = inode
        else:
            self._files[path] = inode

        self._link_count[inode] += 1

    def hardlink(self, source_file: str, destination: str) -> None:
        inode = self._inode_for(source_file)

        if self._is_dir(source_file):
            raise IsADirectoryError(source_file)
        
        if self._is_dir(destination):
            raise NotImplementedError(destination)

        if self._exists(destination):
            raise FileExistsError(destination)

        self._files[destination] = inode
        self._link_count[inode] += 1

    def delete(self, file: str) -> None:
        inode = self._inode_for(file)

        if self._is_dir(file):
            del self._dirs[file]
        elif self.is_file(file):
            del self._files[file]
        else:
            raise FileNotFoundError(file)

        self._link_count[inode] -= 1
        if self._link_count[inode] == 0:
            del self._link_count[inode]
