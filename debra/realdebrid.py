import requests
import json

from types import SimpleNamespace
from typing import List, Dict, Any, Optional

from .exceptions import DebridException
from .error_codes import ERROR_CODES


class Debrid:
    """Real-Debrid API Wrapper"""

    def __init__(self, api_key: str):
        self.url: str = "https://api.real-debrid.com/rest/1.0"
        self.api_key: str = api_key
        self.error_codes: Dict[str, str] = ERROR_CODES
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})

    def _request(self, method: str, endpoint: str, data=None, params=None) -> SimpleNamespace:
        """Send a request to the Real-Debrid API and return response as SimpleNamespace or raise exception."""
        url = f"{self.url}/{endpoint}"
        try:
            response = self.session.request(method, url, data=data, params=params)
            response_data = json.loads(response.content.decode('utf-8'))
            if hasattr(response_data, "error_code"):
                error_message = ERROR_CODES.get(str(response_data.error_code), "Unknown error")
                raise DebridException(f"Real Debrid Code {response_data.error_code}: {error_message}")
            else:
                return response_data
        except requests.exceptions.ConnectTimeout:
            raise DebridException("Connection to Real-Debrid API timed out")
        except requests.exceptions.ConnectionError:
            raise DebridException("Failed to connect to Real-Debrid API")
        except requests.exceptions.JSONDecodeError:
            raise DebridException("Invalid response received from Real-Debrid API")
        except Exception as e:
            raise DebridException("Real-Debrid error: %s", e)

    def user(self) -> SimpleNamespace:
        """Validate the Real-Debrid API key."""
        response = self._request("GET", "user")
        if response:
            data = {
                "id": response.id,
                "username": response.username,
                "email": response.email,
                "premium": response.premium,
                "points": response.points,
                "type": response.type,
                "avatar": response.avatar,
                "expiration": response.expiration,
                "locale": response.locale
            }
            return SimpleNamespace(**data)
        return None

    def validate(self) -> bool:
        """Validate the Real-Debrid API key and user is premium."""
        data = self.user()
        return data.get("premium", 0) > 0 if data else False

    def is_downloaded(self, info_hash: str) -> bool:
        """Check if the given torrent is already downloaded."""
        torrents = self.get_torrents()
        return any(torrent.get("hash") == info_hash for torrent in torrents) if torrents else False

    @staticmethod
    def _chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
        """Chunk a list into smaller lists of a specified size."""
        return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

    def is_cached(self, info_hashes: List[str]) -> Dict[str, Dict[str, float]]:
        """Checks multiple infohashes for cached files on Real-Debrid and returns a dict with filenames and file sizes in MB."""
        cached_files = {}
        for chunk in self._chunk_list(info_hashes, 10):
            response = self._request("GET", f"torrents/instantAvailability/{'/'.join(chunk)}")
            if response:
                for info_hash, content in response.items():
                    file_details = {}
                    if content.get("rd", []):
                        for item in content["rd"]:
                            for _, files in item.items():
                                filename = files.get("filename")
                                filesize = files.get("filesize") / 1e+6  # Convert bytes to MB
                                if filename and filesize:
                                    file_details[filename] = filesize
                    if file_details:
                        cached_files[info_hash] = file_details
        return cached_files

    def get_torrents(self, limit=2500) -> List[Dict[str, Any]]:
        """Get the list of torrents from Real-Debrid."""
        return self._request("GET", "torrents", params={"filter": "active", "limit": limit})

    def add_magnet(self, infohash: str) -> str:
        """Add a magnet link to Real-Debrid and return the request ID."""
        magnet = "magnet:?xt=urn:btih:" + infohash + "&dn=&tr="
        response = self._request("POST", "torrents/addMagnet", data={"magnet": magnet})
        return response.id if response else ""

    def remove_torrent(self, request_id: str) -> bool:
        """Remove a torrent from Real-Debrid."""
        response = self._request("DELETE", f"torrents/delete/{request_id}")
        return True if response else False

    def select_files(self, request_id: str, files: List[str]) -> bool:
        """Select files for download from Real-Debrid."""
        response = self._request("POST", f"torrents/selectFiles/{request_id}", data={"files": files})
        return True if response else False

    def get_torrent_info(self, request_id: str) -> Optional[SimpleNamespace]:
        """Get information about a torrent from Real-Debrid."""
        response = self._request("GET", f"torrents/info/{request_id}")
        return response if response else None
