"""Functions for working with API."""


import json
import logging
from enum import Enum

import requests
from requests.exceptions import ConnectionError

from yadicm.config import (
    API_SANDBOX_MODE,
    API_CAMPAIGNS_URL,
    API_SANDBOX_CAMPAIGNS_URL,
)
from yadicm.helpers import (
    get_filepath_for_user_campaigns,
    read_campaigns_from_file,
    write_campaigns_to_file,
)


class APIMethods(Enum):
    """API Methods."""
    GET = {
        "method": "get",
        "result": "Campaigns",
        "ok_msg": "Идентификаторы кампаний записаны в {}.",
    }
    SUSPEND = {
        "method": "suspend",
        "result": "SuspendResults",
        "ok_msg": "Кампании остановлены.",
    }
    RESUME = {
        "method": "resume",
        "result": "ResumeResults",
        "ok_msg": "Кампании запущены.",
    }


def send_request(
    user_access_token: str, body: dict
) -> requests.Response | None:
    """Send a request to the API."""
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
    json_body = json.dumps(body, ensure_ascii=False).encode("utf8")

    try:
        response = requests.post(api_url, json_body, headers=headers)
        logging.debug(
            f"Заголовки запроса: {response.request.headers}.\n"
            f"Запрос: {response.request.body}.\n"
            f"Заголовки ответа: {response.headers}.\n"
            f"Ответ: {response.text}."
        )
        response_json = response.json()
        error = response_json.get("error", False)
        if response.status_code != 200 or error:
            error_code = error.get("error_code", "")
            error_detail = error.get("error_detail", "")
            error_string = error.get("error_string", "")
            error_description = error_detail or error_string
            request_id = response.headers.get("RequestId", False)
            logging.error(
                "Произошла ошибка при обращении к серверу API Директа.\n"
                f"Код ошибки: {error_code}.\n"
                f"Описание ошибки: {error_description}.\n"
                f"RequestId: {request_id}."
            )
            return
        else:
            return response
            
    except ConnectionError:
        logging.error("Произошла ошибка соединения с сервером API.")
    except:
        logging.error("Произошла непредвиденная ошибка.")


def get_campaigns(user_access_token: str, username: str) -> None:
    """Get campaigns list for user."""
    body = {
        "method": APIMethods.GET.value.get("method", ""),
        "params": {
            "SelectionCriteria": {},
            "FieldNames": ["Id", "Name"],
        }
    }
    response = send_request(user_access_token, body)
    if response:
        response_json = response.json()
        request_id = response.headers.get("RequestId", False)
        units = response.headers.get("Units", False)
        logging.debug(
            f"RequestId: {request_id}.\n"
            f"Информация о баллах: {units}."
        )
        result = response_json.get("result", {})
        campaigns = result.get(APIMethods.GET.value.get("result"))
        if not result or not campaigns:
            logging.error("В ответе сервера API нет списка кампаний.")
            return
        filepath = get_filepath_for_user_campaigns(username)
        write_campaigns_to_file(campaigns, filepath)
        logging.info(APIMethods.GET.value.get("ok_msg", "{}").format(filepath))


def change_campaigns_state(
    user_access_token: str, username: str, api_method: APIMethods
) -> None:
    """Suspend user's campaigns."""
    filepath = get_filepath_for_user_campaigns(username)
    campaigns = read_campaigns_from_file(filepath)
    body = {
        "method": api_method.value.get("method", ""),
        "params": {
            "SelectionCriteria": {
                "Ids": campaigns
            },
        }
    }
    response = send_request(user_access_token, body)
    if response:
        response_json = response.json()
        request_id = response.headers.get("RequestId", False)
        units = response.headers.get("Units", False)
        logging.debug(
            f"RequestId: {request_id}.\n"
            f"Информация о баллах: {units}."
        )
        result = response_json.get("result", {})
        result_list = result.get(api_method.value.get("result"))
        if not result or not result_list:
            logging.error("В ответе сервера API нет результатов выполнения.")
        else:
            logging.info(api_method.value.get("ok_msg"))
