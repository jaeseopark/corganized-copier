import io
import os

import yaml
from commmons import merge

_OVERRIDE_PATH = "/shared/config.yml"

_DEFAULT = """
basic:
  log_path: /shared/copier.log
  backup:
    path: /backup
    default_ext: dec
    mimetype_ext_override:
      application/zip: zdec
  pool_size: 3
  files_per_run: 1000
  max_filesize: 1500000000 # 1.5 GB
server:
  host: ""
  apikey: ""
download:
  path: /tmp/downloads
  max_speed: 5000000  # 5 MB/s per process
  gdrive:
    creds_path: /shared/gdrive_creds.json
"""


def _get_override() -> dict:
    override_path = os.getenv("CONFIG_OVERRIDE_PATH") or _OVERRIDE_PATH
    if os.path.exists(override_path):
        with open(override_path) as fp:
            return yaml.safe_load(fp)
    return dict()


def get_config() -> dict:
    with io.StringIO(_DEFAULT) as fp:
        c = yaml.safe_load(fp)

    return merge(c, _get_override(), dict(server=dict(
        host=os.getenv("CRG_SERVER_HOST"),
        apikey=os.getenv("CRG_SERVER_APIKEY")
    )))
