import os
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
    def size_mb(self):  # mega bytes
        size = 0
        if self.local_path and os.path.exists(self.local_path):
            size = os.stat(self.local_path).st_size
        if "size" in self.file:
            size = self.file["size"]
        return round(size / pow(2, 20))

    @property
    def enc_basename(self):
        return self.fileid + ".aes"

    @property
    def normalized_basename(self):
        mimetype = self.file.get("mimetype")
        default_ext = self.config["basic"]["backup"]["default_ext"]
        dynamic_ext_override = self.config["basic"]["backup"]["dynamic_ext_override"]

        def get_extension() -> str:
            if not mimetype:
                return default_ext
            return dynamic_ext_override.get(mimetype) or mimetype.split('/')[1]

        return f"{self.fileid}.{get_extension()}"

    def __str__(self):
        size = self.size_mb
        return f"status={self.status} {size=}MB local_path={self.local_path}"
