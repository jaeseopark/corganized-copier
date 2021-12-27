import os
from functools import reduce
from itertools import repeat
from multiprocessing import Manager
from multiprocessing.pool import Pool
from threading import Lock
from typing import Callable

import yaml
from commmons import touch_directory, touch, merge
from commmons import with_timer

from copier.config import get_default_config
from copier.downloader.factory import get_download_client
from copier.error import NeglectableError
from copier.job import Job
from copier.treatment.impl import download, move
from copier.utils.cc_wrapper import CorganizeClientWrapper
from copier.utils.mpsafelog import get_mpsafe_logger

TREATMENTS = (download, move)


def get_local_config() -> dict:
    config = get_default_config()
    with open(os.environ["CONFIG_OVERRIDE_PATH"]) as fp:
        return merge(config, yaml.safe_load(fp))


def apply(job: Job, treatment: Callable[[Job], Job]) -> Job:
    try:
        return treatment(job)
    except NeglectableError:
        job.logger.info("A neglectable error has occurred")
        return job
    except Exception:
        # log and move on.
        job.logger.exception("An unknown error has occurred")
        raise StopIteration


def copy_file(file: dict, config: dict, lock: Lock):
    logger = with_timer(get_mpsafe_logger(config))
    cc = CorganizeClientWrapper(config["server"])
    dlcli = get_download_client(file, config["download"])
    job = Job(file, config, logger, cc, dlcli, lock)

    try:
        reduce(apply, TREATMENTS, job)
    except StopIteration:
        pass


def run_copier():
    config = get_local_config()
    touch_directory(config["download"]["path"])
    touch_directory(config["basic"]["backup_path"])
    touch(config["basic"]["log_path"])

    cc = CorganizeClientWrapper(config["server"])

    local_filenames = os.listdir(config["basic"]["backup_path"])
    missing_files = cc.get_missing_files(local_filenames, config=config["basic"])

    lock = Manager().Lock()

    zipped_args = zip(missing_files, repeat(config), repeat(lock))
    with Pool(config["basic"]["pool_size"]) as pool:
        pool.starmap(copy_file, zipped_args)