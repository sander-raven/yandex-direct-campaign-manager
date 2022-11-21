"""Various helper functions."""


import datetime
import logging
from pathlib import Path


def get_logfile_name() -> str:
    return "yadicm_" + datetime.datetime.now().strftime("%Y_%m") + ".log"


def write_campaigns_to_file(campaigns: list, filepath: Path) -> None:
    """Write campaigns from the list to a file."""
    campaigns_id = [
        str(c.get("Id")) for c in campaigns if c.get("Id") is not None
    ]
    filepath.parents[0].mkdir(parents=True, exist_ok=True)
    logging.debug(f"Список ID кампаний: {campaigns_id}.")
    logging.debug(f"Файл для сохранения: {filepath.resolve()}.")
    filepath.write_text(
        "\n".join(campaigns_id)
    )
