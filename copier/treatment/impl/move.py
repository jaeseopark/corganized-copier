import os
import shutil

from copier.job import Job


def move(job: Job) -> Job:
    backup_folder_path = job.config["basic"]["backup_path"]
    target_path = os.path.join(backup_folder_path, job.basename)
    source_path = job.local_path

    def move_safely():
        job.status = "moving"
        shutil.copyfile(source_path, target_path)
        os.remove(source_path)

    if job.is_big_file:
        # Avoid moving big files simultaneously
        with job.lock:
            move_safely()
    else:
        move_safely()

    job.status = "moved"

    return job
