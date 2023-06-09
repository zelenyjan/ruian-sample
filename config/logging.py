from __future__ import annotations

import logging

from colorama import Fore, Style


class RuianFormatter(logging.Formatter):
    template = "[{levelname}][{asctime}][{name}][{module}][{lineno}][{process:d}][{thread:d}]|{message}"

    def get_template(self, record: logging.LogRecord) -> str:
        return self.template

    def format(self, record: logging.LogRecord) -> str:  # noqa: A003
        log_fmt = self.get_template(record)
        formatter = logging.Formatter(log_fmt, style="{")
        return formatter.format(record)


class ColoramaFormatter(RuianFormatter):
    config = {
        logging.CRITICAL: Fore.RED,
        logging.ERROR: Fore.MAGENTA,
        logging.WARNING: Fore.YELLOW,
        logging.INFO: Fore.GREEN,
        logging.DEBUG: Fore.WHITE,
    }

    def get_template(self, record: logging.LogRecord) -> str:
        if record.levelno in self.config:
            # build template
            return f"{self.config[record.levelno]}{self.template}{Style.RESET_ALL}"
        return super().get_template(record)
