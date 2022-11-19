"""Application entry point."""


import logging

import yadicm.config as cfg


if __name__ == "__main__":
    logging.info(f"Начало работы {cfg.APP_NAME} (v{cfg.APP_VERSION}).")
    logging.info(f"{cfg.API_SANDBOX_MODE=}")
    logging.info(f"Завершение работы {cfg.APP_NAME} (v{cfg.APP_VERSION}).")
