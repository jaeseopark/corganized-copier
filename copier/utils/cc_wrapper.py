from typing import List

from commmons import now_seconds
from corganizeclient.client import CorganizeClient

from copier.downloader.factory import is_supported

# This number is set much higher than 'files_per_run' to avoid getting stuck with undownloadable files.
QUERY_LIMIT = 1000


class CorganizeClientWrapper(CorganizeClient):
    def __init__(self, server_config: dict):
        super().__init__(server_config["host"], server_config["apikey"])

    def get_missing_files(self, local_filenames: List[str], config: dict):
        limit: int = config["files_per_run"]
        max_filesize: int = config["max_filesize"]

        def is_missing_locally(file: dict) -> bool:
            is_encrypted_file_missing = file["fileid"] + ".aes" not in local_filenames
            is_decrypted_file_missing = file["fileid"] + ".dec" not in local_filenames
            is_decrypted_zip_file_missing = file["fileid"] + ".zdec" not in local_filenames
            return is_encrypted_file_missing and (is_decrypted_file_missing or is_decrypted_zip_file_missing)

        def is_downloadable(file: dict) -> bool:
            return is_supported(file.get("storageservice"))

        def is_adequate_size(file: dict) -> bool:
            return file.get("size", 0) < max_filesize

        def is_active(file: dict) -> bool:
            return file.get("dateactivated", 0) > 0

        active_files = self.get_stale_files(limit=QUERY_LIMIT)
        missing = [file for file in active_files if
                   is_missing_locally(file) and is_downloadable(file) and is_adequate_size(file) and is_active(file)]
        return missing[:limit]
