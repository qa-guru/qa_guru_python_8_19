import jsonschema
import pytest
import requests
from requests import Response

from utils import load_schema


def test_get_single_user_successfully():
    url = "https://reqres.in/api/users/2"
    schema = load_schema("get_single_user.json")

    result: Response = requests.get(url)

    assert result.status_code == 200
    jsonschema.validate(result.json(), schema)


@pytest.mark.parametrize('id_', [1, 2, 3])
def test_get_single_user_id(id_):
    url = f"https://reqres.in/api/users/{id_}"

    result = requests.get(url)
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

    result = requests.get(
        url=url,
        params={"page": page, "per_page": per_page}
    )

    assert result.json()["per_page"] == per_page
    assert len(result.json()['data']) == per_page
