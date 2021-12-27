from copier.downloader.gdrive import CustomerGDriveWrapper
from copier.downloader.interface import DownloadClient

_DOWNLOAD_CLIENTS = {
    "gdrive": CustomerGDriveWrapper
}


def get_download_client(file: dict, download_config: dict) -> DownloadClient:
    storageservice = file["storageservice"]
    cls = _DOWNLOAD_CLIENTS.get(storageservice)
    if not cls:
        raise ValueError(f"No download client for {storageservice=}")

    return cls(download_config)


def is_supported(storage_service: str) -> bool:
    return storage_service in _DOWNLOAD_CLIENTS
