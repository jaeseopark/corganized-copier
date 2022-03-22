from copier.job import Job
import os

import pyAesCrypt

BUFFER_SIZE = 65536


def decrypt(job: Job) -> Job:
    job.status = "decrypting"

    aes_key = job.config["remote"]["aeskey"]
    assert aes_key and isinstance(aes_key, str)

    dec_path = job.local_path + ".dec"

    pyAesCrypt.decryptFile(job.local_path, dec_path, aes_key, BUFFER_SIZE)

    os.remove(job.local_path)
    job.local_path = dec_path

    job.status = "decrypted"
    return job
