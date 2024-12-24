import requests

class UserApi:
    BASE_URL = "https://jsonplaceholder.typicode.com"

    def get_user(self, user_id):
        """Fetches a user by their ID."""
        url = f"{self.BASE_URL}/users/{user_id}"
        response = requests.get(url)
        response.raise_for_status()  # Will raise an HTTPError for bad status codes
        return response.json()

    def create_user(self, name, username, email):
        """Creates a new user."""
        url = f"{self.BASE_URL}/users"
        payload = {"name": name, "username": username, "email": email}
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    def update_user(self, user_id, name, username, email):
        """Updates an existing user."""
        url = f"{self.BASE_URL}/users/{user_id}"
        payload = {"name": name, "username": username, "email": email}
        response = requests.put(url, json=payload)
        response.raise_for_status()
        return response.json()
