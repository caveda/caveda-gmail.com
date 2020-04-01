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
    parser.add_argument('--filetoken', dest='filetoken', default=None,
                        help='File containing the auth token. Required when Storage has restrictive rules')
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


def initialize_firebase(config_file):
    """ Loads the content of the configuration json file into Pyrebase. Returns instances of used services """
    configuration = load_config_as_dict(config_file)
    firebase = pyrebase.initialize_app(configuration)
    return firebase.auth(), firebase.storage()


def upload_files_to_storage(storage, remote_path, files, token=None):
    """ Uploads files to remote_path in Firebase storage. """
    for f in files:
        assert file_exists(f), f"File {f} does not exists"
        server_path = path.join(remote_path, path.basename(f))
        log(f"Uploading {f} to {server_path}")
        storage.child(server_path).put(f, token)


def read_token(file_token):
    if file_token is None:
        return None
    assert file_exists(file_token), f"Configuration file {file_token} does not exist"
    with open(file_token) as f:
        token = f.read()
        return token


def sign_in_with_token(auth, filetoken):
    custom_token = read_token(filetoken)
    user = auth.sign_in_with_custom_token(custom_token)
    token = user['idToken']
    return token



def main():
    """ Main function """
    start = time.time()
    init_logging()
    log("Start execution")
    args = parse_arguments()
    auth, storage = initialize_firebase(args.config)
    token = sign_in_with_token(auth, args.filetoken)
    upload_files_to_storage(storage, args.remote_path, args.files, token)
    elapsed = time.time() - start
    log(f"Execution time: {str(timedelta(seconds=elapsed))}")


if __name__ == "__main__":
    main()
