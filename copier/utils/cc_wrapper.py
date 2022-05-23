from typing import List, Iterator

from corganizeclient.client import CorganizeClient

from copier.downloader.factory import is_supported


class CorganizeClientWrapper(CorganizeClient):
    def __init__(self, server_config: dict):
        super().__init__(server_config["host"], server_config["apikey"])

    def get_missing_files(self, local_filenames: List[str], config: dict):
        local_filenames_set = set(local_filenames)
        limit: int = config["files_per_run"]
        max_filesize: int = config["max_filesize"]

        def exists_locally(fileid: str, extensions: List[str]) -> bool:
            return any([f"{fileid}.{ext}" in local_filenames_set for ext in extensions])

        def custom_filter(files: List[dict]) -> List[dict]:
            def iterate() -> Iterator[dict]:
                for file in files:
                    if exists_locally(file["fileid"], ["dec", "zdec"]):
                        return
                    if not is_supported(file.get("storageservice")):
                        return
                    if file.get("size", 0) > max_filesize:
                        return
                    if file.get("dateactivated", 0) == 0:
                        return

                    yield file

            return list(iterate())

        return self.get_stale_files(limit=limit, custom_filter=custom_filter)
