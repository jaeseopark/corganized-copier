# corganized-copier

## Usage

### TLDR

```bash
touch ./mnt/copier.log
docker-compose up --build -d
```

### Authorize corganized-copier to use your Google Drive

1. Paste the following snippet into your terminal (UNIX):
    ```bash
    cat > gdrivelogin.py <<EOF
    from gdrivewrapper import GDriveWrapper
    GDriveWrapper("https://www.googleapis.com/auth/drive", "./mnt/gdrive_creds.json")
    EOF
   
    mkdir mnt
    pip install gdrivewrapper
    python gdrivelogin.py --noauth_local_webserver
    ```
1. Follow the steps in the terminal.
1. Once completed, verify that you have `./mnt/gdrive_creds.json` and `./mnt/gdrive_creds_store.json`
1. Cleanup
    ```bash
    rm gdrivelogin.py
    ```
