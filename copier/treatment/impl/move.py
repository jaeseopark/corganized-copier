import os

from copier.job import Job


def move(job: Job) -> Job:
    backup_folder_path = job.config["basic"]["backup_path"]
    target_path = os.path.join(backup_folder_path, job.basename)
    source_path = job.local_path

    if job.is_big_file:
        # Avoid moving big files at the same time
        with job.lock:
            job.status = "moving"
            os.rename(source_path, target_path)
    else:
        job.status = "moving"
        os.rename(source_path, target_path)

    job.status = "moved"

    return job
