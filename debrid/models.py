from typing import List
from pydantic import BaseModel


class File(BaseModel):
    filename: str
    filesize: int

    @property
    def filesize_mb(self) -> float:
        """Return the file size in megabytes."""
        return self.filesize / 1e+6
    
    def __repr__(self) -> str:
        """Return the string representation of the file."""
        return f"{self.filename} ({self.filesize_mb:.2f} MB)"

    def __eq__(self, other: str) -> bool:
        """Compare the filename to another filename."""
        return self.filename == other
    
    def __hash__(self) -> int:
        """Return the hash of the filename."""
        return hash(self.filename)


class StreamCache(BaseModel):
    infohash: str = ""
    files: List[File] = []

    class Config:
        arbitrary_types_allowed = True

    def __repr__(self) -> str:
        file_list = ', '.join([str(file) for file in self.files])
        return f"{self.infohash}: {file_list}"

    def __getitem__(self, filename: str) -> File:
        """Return the file with the specified filename."""
        return next(file for file in self.files if file == filename)

    def __eq__(self, other: str) -> bool:
        """Compare the infohash to another infohash."""
        return self.infohash == other
    
    def __hash__(self) -> int:
        """Return the hash of the infohash."""
        return hash(self.infohash)
    
    def __contains__(self, other: str) -> bool:
        """Check if the filename is in the cached files."""
        return any(file == other for file in self.files)
    
    def __len__(self) -> int:
        """Return the number of files in the cached files."""
        return len(self.files)

    def __iter__(self) -> File:
        """Iterate through the cached files."""
        return iter(self.files)

    def __add__(self, other: File) -> None:
        """Add a file to the cached files."""
        self.files.append(other)