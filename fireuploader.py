import argparse
import time
import logging
from datetime import timedelta


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
    parser.add_argument('config', nargs='?', help='Path of Firebase configuration file')
    return parser.parse_args()


def main():
    """ Main function """
    start = time.time()
    args = parse_arguments()
    init_logging()
    elapsed = time.time() - start
    log(f"Execution time: {str(timedelta(seconds=elapsed))}")


if __name__ == "__main__":
    main()
