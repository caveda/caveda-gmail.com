import argparse
import json
import sys
import time
import logging
from datetime import timedelta
from os import path

import pyrebase


def init_logging():
    """ Initialize the logging mechanism """
    logging.basicConfig(filename='fireuploader.log',
                        level=logging.INFO,
                        format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')


def log(msg):
    """ Writes msg in the logger output."""
    logging.info(msg)


def parse_arguments():
    """ Parse arguments passed to the script """
    parser = argparse.ArgumentParser(description='File uploader to Firebase Storage.')
    parser.add_argument('config', help='Path of Firebase configuration file.')
    parser.add_argument('--token', dest='token', help='Auth token. Required for Storages with restrictive rules')
    parser.add_argument('remote_path', help='Storage path where files have to be uploaded.')
    parser.add_argument('files', nargs='+', help='File or files to upload.')
    return parser.parse_args()


def load_config_as_dict(config_file):
    """ Receives the json file and returns a dictionary with the values. """
    assert file_exists(config_file), f"Configuration file {config_file} does not exist"
    with open(config_file) as json_file:
        data = json.load(json_file)
        return data


def file_exists(config_file):
    return path.exists(config_file) and path.isfile(config_file)


def initialize_firebase_storage(config_file):
    """ Loads the content of the configuration json file into Pyrebase. Returns an instance of storage. """
    configuration = load_config_as_dict(config_file)
    firebase = pyrebase.initialize_app(configuration)
    return firebase.storage()


def upload_files_to_storage(storage, token, remote_path, files):
    """ Uploads files to remote_path in Firebase storage. """
    for f in files:
        assert file_exists(f), f"File {f} does not exists"
        remote_path = path.join(remote_path, path.basename(f))
        log(f"Uploading {f} to {remote_path}")
        storage.child(remote_path).put(f, token)


def main():
    """ Main function """
    start = time.time()
    args = parse_arguments()
    init_logging()
    storage = initialize_firebase_storage(args.config)
    upload_files_to_storage(storage, args.token, args.remote_path, args.files)
    elapsed = time.time() - start
    log(f"Execution time: {str(timedelta(seconds=elapsed))}")


if __name__ == "__main__":
    main()
