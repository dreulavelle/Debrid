class DebridException(Exception):
    """Base class for exceptions in the Debrid module."""

class ValidationFailed(DebridException):
    """Exception raised when validation of API key fails."""

class DownloadStatusCheckFailed(DebridException):
    """Exception raised when checking download status fails."""

class CacheStatusCheckFailed(DebridException):
    """Exception raised when checking cache status fails."""

class TorrentsFetchFailed(DebridException):
    """Exception raised when fetching torrents fails."""

class MagnetAdditionFailed(DebridException):
    """Exception raised when adding a magnet link fails."""

class FileSelectionFailed(DebridException):
    """Exception raised when selecting files fails."""

class TorrentInfoFetchFailed(DebridException):
    """Exception raised when fetching torrent info fails."""

class APITokenNotProvided(DebridException):
    """Exception raised when the API token is not provided."""

class DebridRequestFailed(DebridException):
    """Exception raised when a request fails."""