import logging

from gdrivewrapper import GDriveWrapper

from copier.downloader.interface import DownloadClient, DownloadRequest

logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.FATAL)

API_SCOPE = "https://www.googleapis.com/auth/drive"


class CustomerGDriveWrapper(DownloadClient):
    def __init__(self, downloda_config: dict):
        gdrive_config = downloda_config["gdrive"]
        self.max_speed = downloda_config["max_speed"]  # bytes per second
        self.gdw: GDriveWrapper = GDriveWrapper(API_SCOPE, gdrive_config["creds_path"])

    def download(self, request: DownloadRequest):
        self.gdw.download_file(request.remote_path, request.target_path, max_bytes_per_second=self.max_speed)
