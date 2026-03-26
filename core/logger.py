# professional logging system
# supports file logging, console output, and different log levels

import logging
import os
from datetime import datetime
from pathlib import Path


class ImageGhostLogger:
    """centralized logging for imageghost"""

    def __init__(self, name='imageghost', log_file=None, verbose=True):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.verbose = verbose

        # prevent duplicate handlers
        if self.logger.handlers:
            return

        # create formatters
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_formatter = logging.Formatter('%(message)s')

        # file handler
        if log_file:
            log_dir = os.path.dirname(log_file) or '.'
            os.makedirs(log_dir, exist_ok=True)

            fh = logging.FileHandler(log_file)
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(file_formatter)
            self.logger.addHandler(fh)

        # console handler
        if verbose:
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            ch.setFormatter(console_formatter)
            self.logger.addHandler(ch)

    def debug(self, msg):
        """debug level message"""
        self.logger.debug(msg)

    def info(self, msg):
        """info level message"""
        if self.verbose:
            self.logger.info(f"[*] {msg}")

    def success(self, msg):
        """success message"""
        if self.verbose:
            self.logger.info(f"[+] {msg}")

    def warning(self, msg):
        """warning message"""
        if self.verbose:
            self.logger.warning(f"[!] {msg}")

    def error(self, msg):
        """error message"""
        if self.verbose:
            self.logger.error(f"[-] {msg}")

    def critical(self, msg):
        """critical error message"""
        if self.verbose:
            self.logger.critical(f"[!!] {msg}")


def get_logger(name='imageghost', log_file=None, verbose=True):
    """get or create logger instance"""
    return ImageGhostLogger(name, log_file, verbose)
