from dataclasses import dataclass, field
from logging import LoggerAdapter, Logger
from threading import Lock
from typing import Union

from commmons import with_prefix
from corganizeclient.client import CorganizeClient

from copier.downloader.interface import DownloadClient


@dataclass
class Job(object):
    file: dict
    config: dict
    logger: Union[Logger, LoggerAdapter]
    corganize_client: CorganizeClient
    download_client: DownloadClient
    lock: Lock

    fileid: str = field(default=None)
    local_path: str = field(default=None)
    _status: str = field(default="pending")

    def __post_init__(self):
        fileid = self.file["fileid"]
        self.fileid = fileid
        self.logger = with_prefix(self.logger, f"{fileid=}")

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value: str):
        self._status = value
        self.logger.info(self)

    @property
    def size(self):
        return round(self.file.get("size", 0) / pow(2, 20))

    @property
    def basename(self):
        return self.fileid + ".aes"

    @property
    def is_big_file(self):
        if "size" not in self.file:
            return True
        return self.file["size"] > self.config["basic"]["big_file_threshold"]

    def __str__(self):
        return f"status={self.status} size={self.size}MB local_path={self.local_path}"
