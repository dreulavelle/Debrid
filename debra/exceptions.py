class DebridException(Exception):
    """Base class for exceptions in the Debrid module."""
    pass

class ValidationFailed(DebridException):
    """Exception raised when validation of API key fails."""
    pass

class DownloadStatusCheckFailed(DebridException):
    """Exception raised when checking download status fails."""
    pass

class CacheStatusCheckFailed(DebridException):
    """Exception raised when checking cache status fails."""
    pass

class TorrentsFetchFailed(DebridException):
    """Exception raised when fetching torrents fails."""
    pass

class MagnetAdditionFailed(DebridException):
    """Exception raised when adding a magnet link fails."""
    pass

class FileSelectionFailed(DebridException):
    """Exception raised when selecting files fails."""
    pass

class TorrentInfoFetchFailed(DebridException):
    """Exception raised when fetching torrent info fails."""
    pass

class APITokenNotProvided(DebridException):
    """Exception raised when the API token is not provided."""
    pass
