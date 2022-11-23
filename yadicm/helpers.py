"""Various helper functions."""


import logging
from pathlib import Path

from yadicm.config import FILES_DIR, API_SANDBOX_MODE


def get_filepath_for_user_campaigns(username: str) -> Path:
    """Get filepath for user campaigns."""
    if API_SANDBOX_MODE:
        filename = f"{username}_sandbox_campaigns_list.txt"
    else:
        filename = f"{username}_campaigns_list.txt"
    filepath = Path.joinpath(FILES_DIR, filename)
    return filepath


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


def read_campaigns_from_file(filepath: Path) -> list:
    """Read campaigns from file to list."""
    text = filepath.read_text()
    campaigns = [*map(int, text.split("\n"))]
    return campaigns
