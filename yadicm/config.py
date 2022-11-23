"""Application configuration file."""


from datetime import datetime
import logging.config
import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


APP_NAME = "Yandex Direct Campaign Manager"
APP_VERSION = "0.1.0"

MAIN_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = MAIN_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
FILES_DIR = MAIN_DIR / "files"
FILES_DIR.mkdir(exist_ok=True)

USER_ACCESS_TOKEN_TEMPLATE = "ACCESS_TOKEN_"
OAUTH_TOKEN_URL = os.getenv("OAUTH_TOKEN_URL")

try:
    API_SANDBOX_MODE = int(os.getenv("API_SANDBOX_MODE", "1"))
except (TypeError, ValueError):
    API_SANDBOX_MODE = 1
API_CAMPAIGNS_URL = os.getenv("API_CAMPAIGNS_URL")
API_SANDBOX_CAMPAIGNS_URL = os.getenv("API_SANDBOX_CAMPAIGNS_URL")

logfile_name = "yadicm_" + datetime.now().strftime("%Y_%m") + ".log"

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
            "level": "INFO",
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
