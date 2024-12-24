import json
import os
import time
from configparser import ConfigParser

import pytest
import requests
from oauthlib.common import urlencode
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import xml.etree.ElementTree as ET  # For parsing XML responses


def read_config():
    config = ConfigParser()
    config_file = os.path.join(os.path.dirname(__file__), 'config.ini')
    print(f"Attempting to read config file at: {config_file}")
    config.read(config_file)
    if not config.sections():
        raise Exception(f"Config file not found or is empty: {config_file}")
    print(f"Config sections found: {config.sections()}")
    return config


@pytest.fixture(scope="module")
def driver():
    # Setup: Initialize the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(10)  # Set implicit wait
    yield driver
    driver.quit()  # Teardown: Quit the WebDriver


@pytest.fixture(scope="module")
def config():
    return read_config()


# Test Configuration
# API_URL = API_URLl  # Replace with your API endpoint
# API_KEY = API_KEYy  # Replace with your actual API key

# Step 1: Define the POST request test
def test_post_request(config, driver):
    url = config.get('api', 'API_URL')
    key = config.get('api', 'API_KEY')
    email = config.get('api', 'email')

    headers = {
        "x-api-key": key,
        "Content-Type": "application/json"
    }

    # JSON Body
    payload = {
        "email": email
    }

    response = requests.post(url, json=payload, headers=headers)
    status_code=response.status_code
    print(status_code)
    assert status_code==404
    print(response.json())

    driver.get("https://yopmail.com/en/")
    time.sleep(5)
    driver.find_element(By.XPATH, "//input[@id='login']").send_keys(email)
    time.sleep(10)
    driver.find_element(By.XPATH, "//i[@class='material-icons-outlined f36']").click()
    time.sleep(5)

    # Step 3: Validate the Response
    # assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
    # assert response.json().get("email") == "usery10@yopmail.com", "Email in response doesn't match"

    # Additional Validations (if needed)
    # e.g., Check if response contains specific keys or values
    # assert "message" in response.json(), "Response body does not contain 'message'"
    # assert response.json().get("status") == "success", "Expected status 'success' in the response"


def test_demo_api(config):
    url = config.get('api', 'demourl')

    headers = {
        "Content-Type": "application/json"
    }

    # JSON Body
    payload = {

        "id": 0,
        "category": {
            "id": 0,
            "name": "string"
        },
        "name": "doggie",
        "photoUrls": [
            "string"
        ],
        "tags": [
            {
                "id": 0,
                "name": "string"
            }
        ],
        "status": "available"
    }

    # Step 2: Send POST request
    response = requests.post(url, json=payload, headers=headers)
    print(response.status_code)
    print(response.json())
    response_dict = response.json()

    # Step 3: Validate the Response
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
    assert response.json().get("name") == "doggie", "name in response doesn't match"
    category_details = response_dict["category"]
    print("Category Details:", category_details)
    tags = response_dict["tags"]
    tag_id = tags[0]["id"] if tags else None
    print("Tags:", tag_id)


import requests
import xml.etree.ElementTree as ET  # For parsing XML responses


def test_billpay_api(config):
    # Step 1: Get API URL from config
    url = config.get('demo', 'apiurl')

    # Step 2: Define headers, query parameters, and payload
    headers = {
        "Content-Type": "application/json"
    }

    # Query parameters as a dictionary
    params = {
        "accountId": "15675",
        "amount": "3"  # Removed the extra space
    }

    # JSON Body
    payload = {
        "name": "string",
        "address": {
            "street": "string",
            "city": "string",
            "state": "string",
            "zipCode": "string"
        },
        "phoneNumber": "string",
        "accountNumber": 0
    }

    # Step 3: Send POST request
    response = requests.post(url, json=payload, params=params, headers=headers)

    # Step 4: Handle response
    print("Status Code:", response.status_code)


def test_demoa(config):
    urla = config.get("api", "urla")

    # Step 2: Define headers, query parameters, and payload
    headers = {
        "Content-Type": "application/json"
    }

    # # Query parameters as a dictionary
    # params = {
    #     "accountId": "15675",
    #     "amount": "3"  # Removed the extra space
    # }

    # JSON Body
    payload = [
        {
            "id": 0,
            "username": "NIK",
            "firstName": "NIK",
            "lastName": "NIK",
            "email": "NIK",
            "password": "NIK",
            "phone": "NIK",
            "userStatus": 0
        }
    ]

    # Step 3: Send POST request
    response = requests.post(urla, json=payload, headers=headers)

    # Step 4: Handle response
    print("Status Code:", response.status_code)
    status_code = response.status_code
    print(status_code)
    responsea = response.json()
    print(responsea)


def test_get_api(config):
    # Step 1: Get API URL from config
    urlb = config.get('api', 'urlb')

    # Step 2: Define headers, query parameters, and payload
    # headers = {
    #     "Content-Type": "application/json"
    # }

    # Query parameters as a dictionary
    params = {
        "username": "nnn",
        "password": "nnn"  # Removed the extra space
    }

    # Step 3: Send POST request
    response = requests.get(urlb, params=params)

    # Step 4: Handle response
    print("Status Code:", response.status_code)
    responseb = response.json()
    print(responseb)
