"""Application CLI."""


import argparse
import logging
import os

from yadicm.config import (
    APP_NAME, APP_VERSION, OAUTH_TOKEN_URL, USER_ACCESS_TOKEN_TEMPLATE
)


def main():
    args = parse_cmd_line_arguments()
    user_access_token = get_user_access_token(args.username)
    if user_access_token is None:
        return


def parse_cmd_line_arguments():
    parser = argparse.ArgumentParser(
        prog="yadicm",
        description="Менеджер кампаний Яндекс.Директ.",
    )
    parser.version = f"{APP_NAME} v{APP_VERSION}"
    parser.add_argument("-v", "--version", action="version")
    parser.add_argument(
        "username",
        type=str,
        help="Имя пользователя",
    )
    return parser.parse_args()


def get_user_access_token(username: str) -> str | None:
    env_variable_name = USER_ACCESS_TOKEN_TEMPLATE + username.upper()
    user_access_token = os.getenv(env_variable_name)
    if user_access_token is None:
        logging.error(
            f"Не найден токен для пользователя {username}!\n"
            f"1) Перейдите на страницу {OAUTH_TOKEN_URL}.\n"
            "2) Разрешите доступ приложению.\n"
            f"3) Сохраните полученный токен в переменной окружения"
            f" с названием {env_variable_name}."
        )
    else:
        logging.debug(f"{env_variable_name}={user_access_token}.")
    return user_access_token
