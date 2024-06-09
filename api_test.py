import logging
from typing import Optional

import requests
from pydantic import BaseModel
from pydantic_settings import BaseSettings

log = logging.getLogger(__name__)


class Config(BaseSettings):
    api_url: str = "https://api.e3.cpressland.io"


config = Config()


class User(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    telephone: str


default_users = [
    User(username="lydia", email="lydia@yogscast.com", telephone="123456789"),
    User(username="duncan", email="duncan@yogscast.com", telephone="123456789"),
    User(username="sips", email="sips@yogscast.com", telephone="123456789"),
    User(username="bouphe", email="bouphe@yogscast.com", telephone="123456789"),
]


def test_cleanup_users() -> None:
    log.info("Cleaning up users")
    [requests.delete(f"{config.api_url}/users/{user['id']}") for user in requests.get(f"{config.api_url}/users").json()]


def test_create_users() -> None:
    for user in default_users:
        response = requests.post(f"{config.api_url}/users", json=user.model_dump(exclude_none=True))
        json = response.json()
        assert response.status_code == 201
        user.id = json["id"]
        log.info(f"Created user {user}")


def test_get_each_user() -> None:
    for user in default_users:
        response = requests.get(f"{config.api_url}/users/{user.id}")
        json = response.json()
        assert response.status_code == 200
        assert json == user.model_dump()
        log.info(f"Found user: {user}")


def test_get_user() -> None:
    response = requests.get(f"{config.api_url}/users")
    users = response.json()
    assert len(users) == len(default_users)
    log.info(f"Found {len(users)} users")


def test_update_user() -> None:
    for user in default_users:
        og_email = user.email
        user.email = user.email.replace("yogscast", "hatfilms")
        response = requests.put(f"{config.api_url}/users/{user.id}", json=user.model_dump())
        json = response.json()
        assert response.status_code == 200
        assert json == user.model_dump()
        log.info(f"Updated user {user.id} email from {og_email} to {user.email}")


def test_delete_user() -> None:
    for user in default_users:
        response = requests.delete(f"{config.api_url}/users/{user.id}")
        assert response.status_code == 200
        log.info(f"Deleted user {user.id}")
