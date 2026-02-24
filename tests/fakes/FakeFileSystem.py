from collections import Counter

from application import (
    FileSystemDestinationExistsButDifferentFile,
    FileSystemSourceFileIsDirectory,
    FileSystemFileMissing,
    HardlinkCapable,
    FileDeletionCapable,
    FileExistenceCheckCapable,
)

class FakeFileSystem(
    HardlinkCapable,
    FileDeletionCapable,
    FileExistenceCheckCapable,
):
    def __init__(self):
        self._files: dict[str, int] = {}
        self._dirs: dict[str, int] = {}
        self._link_count: Counter[int] = Counter()
        self._next_inode = 1

    def _exists(self, path: str) -> bool:
        return path in self._files or path in self._dirs

    def _is_file(self, file: str) -> bool:
        return file in self._files
    
    def _is_dir(self, path: str) -> bool:
        return path in self._dirs
    
    def _inode(self, path: str) -> int | None:
        return self._inode_for(path)
    
    def _inode_for(self, path: str) -> int | None:
        if self._is_file(path):
            return self._files[path]
        if self._is_dir(path):
            return self._dirs[path]
        return None
    
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

    def assert_file_existence(self, file: str) -> None:
        if not file in self._files:
            raise FileSystemFileMissing(file)
        return

    def hardlink(self, source_file: str, destination: str) -> None:
        inode = self._inode_for(source_file)
        if inode:
            if self._is_dir(source_file):
                raise FileSystemSourceFileIsDirectory("hardlink", source_file)
            
            if self._is_dir(destination):
                raise NotImplementedError(destination)
            
            if self._exists(destination):
                # Check if it's already a hardlink to src and quietly return to support idempotency
                if self._inode(destination) == self._inode(source_file):
                    return
                else:
                    raise FileSystemDestinationExistsButDifferentFile(destination)
        

            self._files[destination] = inode
            self._link_count[inode] += 1
        else:
            raise FileSystemFileMissing(source_file)

    def delete(self, file: str) -> None:
        inode = self._inode_for(file)

        if self._is_dir(file):
            raise FileSystemSourceFileIsDirectory("delete", file)
        elif self._is_file(file):
            del self._files[file]
        else:
            return # Idempotent success
        
        if inode:
            self._link_count[inode] -= 1
            if self._link_count[inode] == 0:
                del self._link_count[inode]
