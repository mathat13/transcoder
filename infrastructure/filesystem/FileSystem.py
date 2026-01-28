from pathlib import Path

from application import (
    DestinationExistsButDifferentFile,
    SourceFileMissing,
    SourceFileIsDirectory,
    FileSystemIOError,
)

class FileSystem:
    def is_file(self, file: str) -> bool:
        return Path(file).is_file()
    
    def delete(self, file: str) -> None:
        """
        Deletes files only, directories raise an exception.
        """
        input_file = Path(file)

        if not input_file.exists():
            return # Idempotent success

        if input_file.is_dir():
            raise SourceFileIsDirectory("delete", input_file.as_posix())

        try:
            input_file.unlink()
        except OSError as e:
            raise FileSystemIOError("delete", input_file.as_posix(), e)

    def hardlink(self, source_file: str, destination: str) -> None:
        """
        Hardlinks destination to source_file, 
        features auto-append source_file to destination if destination is am existing directory.
        
        :param source_file: String of source file (must be a file!)
        :type source_file: str
        :param destination: Destination file/ dir, if dir, src.name is appended to dir destination
        :type destination: str
        """
        src = Path(source_file)
        dest = Path(destination)

        if src.is_dir():
            raise SourceFileIsDirectory("hardlink", src.as_posix())
        
        if not src.is_file():
            raise SourceFileMissing(src.as_posix())
        
        if dest.is_dir():
            dest = dest / src.name

        if dest.exists():
            try:
                if dest.stat().st_ino == src.stat().st_ino:
                    return  # idempotent success
                else:
                    raise DestinationExistsButDifferentFile(dest.as_posix())
            except OSError as e:
                raise FileSystemIOError("stat", dest.as_posix(), e)
        
        try:
            dest.hardlink_to(src)
        except OSError as e:
            raise FileSystemIOError("hardlink", dest.as_posix(), e)

        
