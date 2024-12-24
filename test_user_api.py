import pytest
from unittest import mock

import requests

from user_api import UserApi


class TestUserApi:
    @mock.patch("user_api.requests.get")
    def test_get_user_success(self, mock_get):
        # Arrange: Mock a successful API response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"id": 1, "name": "John Doe", "username": "johndoe", "email": "john@example.com"}

        api = UserApi()

        # Act: Call the method
        response = api.get_user(1)

        # Assert: Check if the response is as expected
        assert response["id"] == 1
        assert response["name"] == "John Doe"
        assert response["username"] == "johndoe"
        assert response["email"] == "john@example.com"
        mock_get.assert_called_once_with("https://jsonplaceholder.typicode.com/users/1")

    @mock.patch("user_api.requests.get")
    def test_get_user_failure(self, mock_get):
        # Arrange: Mock a failed API response (404)
        mock_get.return_value.status_code = 404
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")

        api = UserApi()

        # Act & Assert: Ensure the HTTPError is raised
        with pytest.raises(requests.exceptions.HTTPError):
            api.get_user(999)

    @mock.patch("user_api.requests.post")
    def test_create_user_success(self, mock_post):
        # Arrange: Mock a successful creation response
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {"id": 11, "name": "Jane Doe", "username": "janedoe", "email": "jane@example.com"}

        api = UserApi()

        # Act: Call the method
        response = api.create_user("Jane Doe", "janedoe", "jane@example.com")

        # Assert: Check if the response is as expected
        assert response["id"] == 11
        assert response["name"] == "Jane Doe"
        assert response["username"] == "janedoe"
        assert response["email"] == "jane@example.com"
        mock_post.assert_called_once_with(
            "https://jsonplaceholder.typicode.com/users",
            json={"name": "Jane Doe", "username": "janedoe", "email": "jane@example.com"}
        )

    @mock.patch("user_api.requests.put")
    def test_update_user_success(self, mock_put):
        # Arrange: Mock a successful update response
        mock_put.return_value.status_code = 200
        mock_put.return_value.json.return_value = {"id": 1, "name": "John Doe", "username": "johndoe", "email": "john.updated@example.com"}

        api = UserApi()

        # Act: Call the method
        response = api.update_user(1, "John Doe", "johndoe", "john.updated@example.com")

        # Assert: Check if the response is as expected
        assert response["email"] == "john.updated@example.com"
        mock_put.assert_called_once_with(
            "https://jsonplaceholder.typicode.com/users/1",
            json={"name": "John Doe", "username": "johndoe", "email": "john.updated@example.com"}
        )

    @mock.patch("user_api.requests.post")
    def test_create_user_failure(self, mock_post):
        # Arrange: Mock a failed creation response (400)
        mock_post.return_value.status_code = 400
        mock_post.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("400 Bad Request")

        api = UserApi()

        # Act & Assert: Ensure the HTTPError is raised
        with pytest.raises(requests.exceptions.HTTPError):
            api.create_user("Invalid", "invaliduser", "invalid@bademail")

    @mock.patch("user_api.requests.put")
    def test_update_user_failure(self, mock_put):
        # Arrange: Mock a failed update response (404)
        mock_put.return_value.status_code = 404
        mock_put.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")

        api = UserApi()

        # Act & Assert: Ensure the HTTPError is raised
        with pytest.raises(requests.exceptions.HTTPError):
            api.update_user(999, "Nonexistent User", "nonexistent", "nonexistent@example.com")
