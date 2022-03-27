import io

import yaml

_DEFAULT = """
basic:
  log_path: /shared/copier.log
  backup:
    path: /backup
    dynamic_ext_override:
      video/x-matroska: mkv
      video/x-flv: flv
      video/quicktime: mov
      video/x-msvideo: avi
      video/x-ms-wmv: wmv
      video/mpeg: mpeg
  pool_size: 3
  files_per_run: 50
  file_age_threshold: 14  # days
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


def get_default_config() -> dict:
    with io.StringIO(_DEFAULT) as fp:
        return yaml.safe_load(fp)
