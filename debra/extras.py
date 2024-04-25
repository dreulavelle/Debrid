from typing import Any, Dict, List


def is_wanted_format(filename: str) -> bool:
    """Check if the given filename has a wanted format."""
    wanted_formats = [".mkv", ".mp4", ".avi"]
    return any(filename.endswith(format) for format in wanted_formats)

def filter_by_size(files: List[Dict[str, Any]], min_size: int = 40) -> List[Dict[str, Any]]:
    """Filter files by minimum size."""
    return [file for file in files if file.get("filesize", 0) >= min_size * 1024 * 1024]

def remove_duplicates(info_hashes: List[str]) -> List[str]:
    """Remove duplicate info hashes from the list."""
    return list(set(info_hashes))