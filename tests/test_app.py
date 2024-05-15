from http import HTTPStatus

import pytest
from fastapi import HTTPException

from fast_zero.app import validate_user_id


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get("/")  # Act

    assert response.status_code == HTTPStatus.OK  # Assert

    assert response.json() == {"message": "Olá Mundo!"}  # Assert


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "secret",
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "username": "alice",
        "email": "alice@example.com",
        "id": 1,
    }


def test_read_users(client):
    response = client.get("/users/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "users": [
            {
                "username": "alice",
                "email": "alice@example.com",
                "id": 1,
            }
        ]
    }


def test_update_user(client):
    response = client.put(
        "/users/1",
        json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "mynewpassword",
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "bob",
        "email": "bob@example.com",
        "id": 1,
    }


def test_put_should_return_404_when_the_id_is_invalid(client):
    response = client.put(
        "/users/404404",
        json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "mynewpassword",
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_delete_should_return_404_when_the_id_is_invalid(client):
    response = client.delete("/users/404404")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_get_user(client):
    response = client.get("/user/1")

    assert response.status_code == HTTPStatus.OK


def test_delete_user(client):
    response = client.delete("/users/1")

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {"message": "User deleted"}


def get_user_should_return_404_when_the_id_is_invalid(client):
    response = client.get("/user/404404")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


@pytest.mark.parametrize("invalid_id", [-1, 0.1, 10000, "XX", None])
def validade_user_id_should_raise_httpexception_when_invalid_id(invalid_id):
    with pytest.raises(HTTPException):
        validate_user_id(invalid_id)
