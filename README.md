# Firestorage-publisher

Python CLI to publish files in Firebase storage

## Usage
```
usage: fireuploader.py [-h] [--filetoken FILETOKEN]
                       config remote_path files [files ...]

File uploader to Firebase Storage.

positional arguments:
  config                Path of Firebase configuration file.
  remote_path           Storage path where files have to be uploaded.
  files                 File or files to upload.

optional arguments:
  -h, --help            show this help message and exit
  --filetoken FILETOKEN
                        File containing the auth token. Required when Storage
                        has restrictive rules

```
