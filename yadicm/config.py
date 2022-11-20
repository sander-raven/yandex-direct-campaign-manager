"""Application configuration file."""


import logging.config
import os
from pathlib import Path

from dotenv import load_dotenv

from yadicm.helpers import get_logfile_name


load_dotenv()


APP_NAME = "Yandex Direct Campaign Manager"
APP_VERSION = "0.1.0"
MAIN_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = MAIN_DIR / "logs"

USER_ACCESS_TOKEN_TEMPLATE = "ACCESS_TOKEN_"
OAUTH_TOKEN_URL = os.getenv("OAUTH_TOKEN_URL")

try:
    API_SANDBOX_MODE = int(os.getenv("API_SANDBOX_MODE", "1"))
except (TypeError, ValueError):
    API_SANDBOX_MODE = 1


logfile_name = get_logfile_name()

LOGGING_CONFIG = {
    "version": 1,

    "formatters": {
        "default_formatter": {
            "format": "[%(levelname)s : %(name)s : %(asctime)s] %(message)s"
        },
    },

    "handlers": {
        "stream_handler": {
            "class": "logging.StreamHandler",
            "formatter": "default_formatter",
        },
        "file_handler": {
            "class": "logging.FileHandler",
            "formatter": "default_formatter",
            "filename": LOG_DIR / logfile_name,
        },
    },

    "loggers": {
        "root": {
            "handlers": [
                "stream_handler",
                "file_handler",
            ],
            "level": "DEBUG",
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
