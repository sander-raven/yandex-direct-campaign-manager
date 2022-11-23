"""Application CLI."""


import argparse
import logging
import os

from yadicm.api import (
    APIMethods,
    get_campaigns,
    change_campaigns_state,
)
from yadicm.config import (
    APP_NAME, APP_VERSION, OAUTH_TOKEN_URL, USER_ACCESS_TOKEN_TEMPLATE
)


def main():
    logging.info("НАЧАЛО РАБОТЫ ПРОГРАММЫ...")
    args = parse_cmd_line_arguments()
    user_access_token = get_user_access_token(args.username)
    if user_access_token is None:
        return
    if args.get:
        get_campaigns(user_access_token, args.username)
    elif args.resume:
        change_campaigns_state(
            user_access_token,
            args.username,
            APIMethods.RESUME,
        )
    elif args.suspend:
        change_campaigns_state(
            user_access_token,
            args.username,
            APIMethods.SUSPEND,
        )
    else:
        logging.error("При вызове скрипта не была передана команда.")
    logging.info("ПРОГРАММА ЗАВЕРШИЛА СВОЮ РАБОТУ.")


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
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-g",
        "--get",
        action="store_true",
        help="Получить список кампаний",
    )
    group.add_argument(
        "-r",
        "--resume",
        action="store_true",
        help="Запустить кампании",
    )
    group.add_argument(
        "-s",
        "--suspend",
        action="store_true",
        help="Остановить кампании",
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
