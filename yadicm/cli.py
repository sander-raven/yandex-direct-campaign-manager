"""Application CLI."""


import argparse

from yadicm.config import APP_NAME, APP_VERSION


def main():
    args = parse_cmd_line_arguments()


def parse_cmd_line_arguments():
    parser = argparse.ArgumentParser(
        prog="yadicm",
        description="Менеджер кампаний Яндекс.Директ.",
    )
    parser.version = f"{APP_NAME} v{APP_VERSION}"
    parser.add_argument("-v", "--version", action="version")
    return parser.parse_args()
