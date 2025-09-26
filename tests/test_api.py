import allure
import pytest

from utils.api_client import ApiClient

BASE_URL = "https://restful-booker.herokuapp.com"


@pytest.fixture
def api_client():
    return ApiClient(BASE_URL)


@allure.feature("[api test] Проверка метода проверки работоспособности сервера")
@allure.story("Позитивный тест")
def test_ping_health_check(api_client):
    with (allure.step("Отправить GET запрос ping")):
        response = api_client.get("/ping")

    with allure.step("Проверка ответа"):
        assert response.status_code == 201


@allure.feature("[api test] Проверка генерации токена при авторизации")
@allure.story("Позитивный тест")
def test_create_token(api_client):
    token = generate_token(api_client)
    assert token is not None


@allure.feature("[api test] Проверка получения списка всех бронирований")
@allure.story("Позитивный тест")
def test_get_all_booking_ids(api_client):
    with allure.step("Отправить GET запрос на получение всех идентификаторов бронирования"):
        response = api_client.get("/booking")

    with allure.step("Проверка ответа"):
        assert response.status_code == 200
        json_data = response.json()
        assert isinstance(json_data, list)
        for item in json_data: assert item["bookingid"] is not None


@allure.feature("[api test] Проверка получения бронирования по id")
@allure.story("Позитивный тест")
def test_get_booking_by_id(api_client):
    with allure.step(f"Отправка в базу данных бронирования для работы с ним и получение его id"):
        booking_id = create_booking(api_client)

    with allure.step(f"Отправить GET запрос на получение бронирования с id 1"):
        response = api_client.get(f"/booking/{booking_id}")

    with allure.step("Проверка ответа"):
        assert response.status_code == 200
        json_data = response.json()
        assert json_data["firstname"] is not None and json_data["totalprice"] is not None


@allure.feature("[api test] Проверка создания нового бронирования")
@allure.story("Позитивный тест")
def test_create_booking(api_client):
    created_booking_id = create_booking(api_client)
    assert created_booking_id is not None


@allure.feature("[api test] Проверка полного изменения бронирования")
@allure.story("Позитивный тест")
def test_put_booking(api_client):
    with allure.step(f"Отправка в базу данных бронирования для работы с ним и получение его id"):
        booking_id = create_booking(api_client)

    with (allure.step("Тело запроса на частичное изменение бронирования")):
        data = {
            "firstname": "John",
            "lastname": "Rambo",
            "totalprice": 555,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2018-05-06",
                "checkout": "2020-05-05"
            },
            "additionalneeds": "Breakfast"
        }

        with (allure.step("Заголовки запроса на создание бронирования")):
            headers = {"Content-Type": "application/json",
                       "Accept": "application/json"}

        with (allure.step("Инициализация cookie запроса")):
            auth_token = generate_token(api_client)
            cookies = {
                "token": auth_token
            }

        with allure.step("Отправить PUT запрос на частичное обновление бронирования"):
            response = api_client.put(f"/booking/{booking_id}", data=data, headers=headers, cookies=cookies)

        with allure.step("Проверка ответа"):
            assert response.status_code == 200
            json_data = response.json()
            assert json_data["firstname"] == "John"
            assert json_data["lastname"] == "Rambo"
            assert json_data["totalprice"] == 555
            assert json_data["bookingdates"]["checkin"] == "2018-05-06"
            assert json_data["bookingdates"]["checkout"] == "2020-05-05"


@allure.feature("[api test] Проверка частичного изменения бронирования")
@allure.story("Позитивный тест")
def test_patch_booking(api_client):
    with allure.step(f"Отправка в базу данных бронирования для работы с ним и получение его id"):
        booking_id = create_booking(api_client)

    with (allure.step("Тело запроса на частичное изменение бронирования")):
        data = {
            "firstname": "Donald",
            "lastname": "Prawn",
            "bookingdates": {
                "checkin": "2018-02-02",
                "checkout": "2019-01-02"
            }
        }

        with (allure.step("Заголовки запроса на создание бронирования")):
            headers = {"Content-Type": "application/json",
                       "Accept": "application/json"}

        with (allure.step("Инициализация cookie запроса")):
            auth_token = generate_token(api_client)
            cookies = {
                "token": auth_token
            }

        with allure.step("Отправить PATCH запрос на частичное обновление бронирования"):
            response = api_client.patch(f"/booking/{booking_id}", data=data, headers=headers, cookies=cookies)

        with allure.step("Проверка ответа"):
            assert response.status_code == 200
            json_data = response.json()
            assert json_data["firstname"] == "Donald"
            assert json_data["lastname"] == "Prawn"
            assert json_data["bookingdates"]["checkin"] == "2018-02-02"
            assert json_data["bookingdates"]["checkout"] == "2019-01-02"


@allure.feature("[api test] Проверка частичного изменения бронирования")
@allure.story("Негативный тест")
def test_patch_booking_negative(api_client):
    with allure.step(f"Отправка в базу данных бронирования для работы с ним и получение его id"):
        booking_id = create_booking(api_client)

    with (allure.step("Тело запроса на частичное изменение бронирования")):
        data = {
            "firstname": "Donald",
            "lastname": "Prawn",
            "bookingdates": {
                "checkin": "2018-02-02",
                "checkout": "2019-01-02"
            }
        }

        with (allure.step("Заголовки запроса на создание бронирования")):
            headers = {"Content-Type": "application/json",
                       "Accept": "application/json"}

        with allure.step("Отправить PATCH запрос на частичное обновление бронирования"):
            response = api_client.patch(f"/booking/{booking_id}", data=data, headers=headers)

        with allure.step("Проверка ответа"):
            assert response.status_code == 403


@allure.feature("[api test] Проверка удаления существующего бронирования")
@allure.story("Позитивный тест")
def test_delete_booking(api_client):
    with (allure.step(f"Отправка в базу данных бронирования для работы с ним и получение его id")):
        booking_id = create_booking(api_client)

        with (allure.step("Инициализация cookie запроса")):
            auth_token = generate_token(api_client)
            cookies = {
                "token": auth_token
            }

        with (allure.step("Заголовки запроса на создание бронирования")):
            headers = {"Content-Type": "application/json"}

        with allure.step("Отправить DELETE запрос на удаление бронирования"):
            response = api_client.delete(f"/booking/{booking_id}", headers=headers, cookies=cookies)

        with allure.step("Проверка ответа"):
            assert response.status_code == 201
            assert api_client.get(f"/booking/{booking_id}").status_code == 404


def generate_token(api_client):
    with (allure.step("Тело запроса на создание токена")):
        data = {
            "username": "admin",
            "password": "password123"
        }

    with (allure.step("Заголовки запроса на создание токена")):
        headers = {"Content-Type": "application/json"}

    with allure.step("Отправить POST запрос"):
        response = api_client.post("/auth", data=data, headers=headers)

    assert response.status_code == 200
    return response.json()["token"]


def create_booking(api_client):
    with (allure.step("Тело запроса на создание бронирования")):
        data = {
            "firstname": "Jim",
            "lastname": "Brown",
            "totalprice": 111,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2018-01-01",
                "checkout": "2019-01-01"
            },
            "additionalneeds": "Breakfast"
        }
    with (allure.step("Заголовки запроса на создание бронирования")):
        headers = {"Content-Type": "application/json",
                   "Accept": "application/json"}

    with allure.step("Отправить POST запрос на создание бронирования"):
        response = api_client.post("/booking", data=data, headers=headers)

    with allure.step("Проверка ответа"):
        assert response.status_code == 200
        json_data = response.json()
        assert json_data["bookingid"] is not None
        assert json_data["booking"]["firstname"] == "Jim"
        assert json_data["booking"]["bookingdates"]["checkin"] == "2018-01-01"
        assert json_data["booking"]["additionalneeds"] == "Breakfast"

    return json_data["bookingid"]
