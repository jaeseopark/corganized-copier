import os
import shutil

from copier.job import Job


def move(job: Job) -> Job:
    backup_folder_path = job.config["basic"]["backup_path"]
    target_path = os.path.join(backup_folder_path, job.dec_basename)
    source_path = job.local_path

    # Avoid moving files simultaneously
    with job.lock:
        job.status = "moving"
        shutil.copyfile(source_path, target_path)
        os.remove(source_path)

    job.status = "moved"

    return job
