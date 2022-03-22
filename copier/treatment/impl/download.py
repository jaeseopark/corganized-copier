import os
import time

from copier.downloader.interface import DownloadRequest
from copier.job import Job


def download(job: Job) -> Job:
    job.status = "downloading"

    download_folder_path = job.config["download"]["path"]
    target_path = os.path.join(download_folder_path, job.enc_basename)

    request = DownloadRequest(job.file["locationref"], target_path, job.config["download"])

    start = time.perf_counter()
    job.download_client.download(request)
    elapsed = time.perf_counter() - start

    speed = round(os.stat(target_path).st_size / elapsed / pow(10, 6), 2)
    job.logger.info(f"{speed=} MB/s")

    job.local_path = target_path

    job.status = "downloaded"

    return job
