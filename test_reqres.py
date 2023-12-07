import json
import logging

import allure
import jsonschema
import pytest
import requests
from allure_commons._allure import step
from allure_commons.types import AttachmentType
from requests import Response

from utils import load_schema


def reqres_api_get(url, **kwargs):
    with step("API Request"):
        result = requests.get(url="https://reqres.in" + url, **kwargs)
        allure.attach(body=json.dumps(result.json(), indent=4, ensure_ascii=True), name="Response", attachment_type=AttachmentType.JSON, extension="json")
        logging.info(result.request.url)
        logging.info(result.status_code)
        logging.info(result.text)
    return result


def test_get_single_user_successfully():
    url = "/api/users/2"
    schema = load_schema("get_single_user.json")

    result: Response = reqres_api_get(url)

    assert result.status_code == 200
    jsonschema.validate(result.json(), schema)


@pytest.mark.parametrize('id_', [1, 2, 3])
def test_get_single_user_id(id_):
    url = f"/api/users/{id_}"

    result = reqres_api_get(url)
    assert result.json()['data']['id'] == id_


def test_list_of_users_pagination():
    page = 2
    url = "https://reqres.in/api/users"

    result = requests.get(url, params={"page": page})

    assert result.json()["page"] == page


def test_list_of_users_per_page():
    page = 2
    per_page = 6
    url = "https://reqres.in/api/users"
    with step("API Request"):
        result = requests.get(
            url=url,
            params={"page": page, "per_page": per_page}
        )
        allure.attach(body=json.dumps(result.json(), indent=4, ensure_ascii=True), name="Response", attachment_type=AttachmentType.JSON, extension="json")
    assert result.json()["per_page"] == per_page
    assert len(result.json()['data']) == per_page
