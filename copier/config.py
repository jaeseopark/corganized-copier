import io

import yaml

_DEFAULT = """
basic:
  log_path: /shared/copier.log
  backup_path: /backup
  pool_size: 3
  files_per_run: 50
  file_age_threshold: 14  # days
  big_file_threshold: 100000000  # 100 MB
server:
  host: ""
  apikey: ""
download:
  path: /tmp/downloads
  max_speed: 5000000  # 5 MB/s per process
  gdrive:
    creds_path: /shared/gdrive_creds.json
"""


def get_default_config() -> dict:
    with io.StringIO(_DEFAULT) as fp:
        return yaml.safe_load(fp)