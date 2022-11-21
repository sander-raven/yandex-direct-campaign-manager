"""Functions for working with API."""


import json
import logging
from pathlib import Path

import requests
from requests.exceptions import ConnectionError

from yadicm.config import (
    API_SANDBOX_MODE,
    API_CAMPAIGNS_URL,
    API_SANDBOX_CAMPAIGNS_URL,
    FILES_DIR,
)
from yadicm.helpers import write_campaigns_to_file


def get_campaigns(user_access_token: str, username: str) -> None:
    """Get campaigns list for user."""
    
    if API_SANDBOX_MODE:
        api_url = API_SANDBOX_CAMPAIGNS_URL
    else:
        api_url = API_CAMPAIGNS_URL
    
    if api_url is None:
        logging.error("Не задана переменная с адресом API.")
        return

    headers = {
        "Authorization": "Bearer " + user_access_token,
        "Accept-Language": "ru",
    }
    body = {
        "method": "get",
        "params": {
            "SelectionCriteria": {},
            "FieldNames": ["Id", "Name"],
        }
    }
    json_body = json.dumps(body, ensure_ascii=False).encode("utf8")

    try:
        result = requests.post(api_url, json_body, headers=headers)
        logging.debug(
            f"Заголовки запроса: {result.request.headers}.\n"
            f"Запрос: {result.request.body}.\n"
            f"Заголовки ответа: {result.headers}.\n"
            f"Ответ: {result.text}."
        )
        result_json = result.json()
        request_id = result.headers.get("RequestId", False)
        error = result_json.get("error", False)
        if result.status_code != 200 or error:
            error_code = error.get("error_code", "")
            error_detail = error.get("error_detail", "")
            error_string = error.get("error_string", "")
            error_description = error_detail or error_string
            logging.error(
                "Произошла ошибка при обращении к серверу API Директа.\n"
                f"Код ошибки: {error_code}.\n"
                f"Описание ошибки: {error_description}.\n"
                f"RequestId: {request_id}."
            )
        else:
            units = result.headers.get("Units", False)
            logging.debug(
                f"RequestId: {request_id}.\n"
                f"Информация о баллах: {units}."
            )
            result = result_json.get("result", {})
            campaigns = result.get("Campaigns")
            if not result or not campaigns:
                logging.error("В ответе сервера API нет списка кампаний.")
                return
            filename = f"{username}_campaigns_list.txt"
            filepath = Path.joinpath(FILES_DIR, filename)
            write_campaigns_to_file(campaigns, filepath)
            logging.info(f"Идентификаторы кампаний записаны в {filepath}.")
    except ConnectionError:
        logging.error("Произошла ошибка соединения с сервером API.")
    except:
        logging.error("Произошла непредвиденная ошибка.")
