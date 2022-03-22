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
        file_age_threshold: int = config["file_age_threshold"]
        limit: int = config["files_per_run"]
        max_filesize: int = config["max_filesize"]

        def is_missing(file: dict):
            is_encrypted_file_missing = file["fileid"] + ".aes" not in local_filenames
            is_decrypted_file_missing = file["fileid"] + ".dec" not in local_filenames
            return is_encrypted_file_missing and is_decrypted_file_missing

        def is_downloadable(file: dict):
            return is_supported(file.get("storageservice"))

        def is_new(file: dict):
            return now_seconds() < file["dateactivated"] + file_age_threshold * 86400

        def is_adequate_size(file: dict):
            return file.get("size", 0) < max_filesize

        active_files = self.get_active_files(limit=QUERY_LIMIT)
        missing = [file for file in active_files if
                   is_missing(file) and is_downloadable(file) and is_new(file) and is_adequate_size(file)]
        return missing[:limit]
