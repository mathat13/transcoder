from pathlib import Path

class FileSystem:
    def is_file(self, file: str) -> bool:
        return Path(file).is_file()
    
    def delete(self, file: str) -> None:
        input_file = Path(file)
        if input_file.is_file():
            input_file.unlink()

    def hardlink(self, source_file: str, destination: str) -> None:
        """
        Hardlinks destination to source_file, 
        features auto-append source_file to destination if destination is am existing directory.
        
        :param source_file: String of source file (must be a file!)
        :type source_file: str
        :param destination: Destination file/ dir, if dir, src.name is appended to dir diestination
        :type destination: str
        """
        src = Path(source_file)
        dest = Path(destination)

        if not src.is_file():
            raise ValueError(f"Source is not a file: {src}")
        
        if dest.is_dir():
            dest = dest / src.name
        
        dest.hardlink_to(src)

        
