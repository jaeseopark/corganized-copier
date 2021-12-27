from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class DownloadRequest:
    remote_path: str
    target_path: str
    download_config: dict


class DownloadClient(ABC):
    @abstractmethod
    def download(self, request: DownloadRequest):
        pass
