from typing import List

from corganizeclient.client import CorganizeClient

from copier.downloader.factory import is_supported

# This number is set much higher than 'files_per_run' to avoid getting stuck with undownloadable files.
QUERY_LIMIT = 50000


class CorganizeClientWrapper(CorganizeClient):
    def __init__(self, server_config: dict):
        super().__init__(server_config["host"], server_config["apikey"])

    def get_missing_files(self, local_filenames: List[str], config: dict):
        local_filenames_set = set(local_filenames)
        limit: int = config["files_per_run"]
        max_filesize: int = config["max_filesize"]

        def is_missing_locally(file: dict) -> bool:
            is_decrypted_file_missing = file["fileid"] + ".dec" not in local_filenames_set
            is_decrypted_zip_file_missing = file["fileid"] + ".zdec" not in local_filenames_set
            return is_decrypted_file_missing and is_decrypted_zip_file_missing

        def is_downloadable(file: dict) -> bool:
            return is_supported(file.get("storageservice"))

        def is_adequate_size(file: dict) -> bool:
            return file.get("size", 0) < max_filesize

        def is_active(file: dict) -> bool:
            return file.get("dateactivated", 0) > 0

        stale_files = self.get_stale_files(limit=QUERY_LIMIT, interval=15)
        missing = [file for file in stale_files if
                   is_missing_locally(file) and is_downloadable(file) and is_adequate_size(file) and is_active(file)]

        return missing[:limit]
