import os
import time

import pytest
from pyautogui import click
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
from configparser import ConfigParser


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
    driver.quit()


@pytest.fixture(scope="module")
def config():
    return read_config()


def test_login(driver, config):
    url = config.get('demo', 'url')
    username = config.get('demo', 'username')
    password = config.get('demo', 'password')
    driver.get(url)
    driver.maximize_window()
    time.sleep(10)
    driver.find_element(By.XPATH, "//input[@name='username']").send_keys(username)
    time.sleep(5)
    driver.find_element(By.XPATH, "//input[@name='password']").send_keys(password)
    time.sleep(5)
    driver.find_element(By.XPATH, "//input[@value='Log In']").click()
    time.sleep(10)
    driver.find_element(By.XPATH, "//a[normalize-space()='Log Out']").click()
    time.sleep(5)


def test_services(driver, config):
    url = config.get('demo', 'url')
    driver.get(url)
    driver.find_element(By.XPATH,
                        "//ul[@class='leftmenu']//li//a[@href='services.htm'][normalize-space()='Services']").click()
    time.sleep(10)


def test_products(driver, config):
    url = config.get('demo', 'url')
    driver.get(url)
    driver.find_element(By.XPATH,
                        "//ul[@class='leftmenu']//a[normalize-space()='Products']").click()
    time.sleep(10)


def test_open_account(driver, config):
    url = config.get('demo', 'url')
    username = config.get('demo', 'username')
    password = config.get('demo', 'password')
    driver.get(url)
    driver.maximize_window()
    time.sleep(10)
    driver.find_element(By.XPATH, "//input[@name='username']").send_keys(username)
    time.sleep(5)
    driver.find_element(By.XPATH, "//input[@name='password']").send_keys(password)
    time.sleep(5)
    driver.find_element(By.XPATH, "//input[@value='Log In']").click()
    time.sleep(10)
    driver.find_element(By.XPATH, "//a[normalize-space()='Open New Account']").click()
    driver.implicitly_wait(10)
    dropdown = Select(driver.find_element("xpath", "//select[@id='type']"))
    dropdown.select_by_visible_text("CHECKING")

    # account = Select(driver.find_element("//select[@id='fromAccountId']"))
    # account.select_by_visible_text("15675")

    time.sleep(5)

    driver.find_element(By.XPATH, "//input[@value='Open New Account']").click()
    time.sleep(5)

def test_account_overview(driver, config):
    url = config.get('demo', 'url')
    username = config.get('demo', 'username')
    password = config.get('demo', 'password')
    driver.get(url)
    driver.maximize_window()
    time.sleep(10)
    driver.find_element(By.XPATH, "//input[@name='username']").send_keys(username)
    time.sleep(5)
    driver.find_element(By.XPATH, "//input[@name='password']").send_keys(password)
    time.sleep(5)
    driver.find_element(By.XPATH, "//input[@value='Log In']").click()
    time.sleep(10)
    driver.find_element(By.XPATH, "//a[normalize-space()='Accounts Overview']").click()
    time.sleep(5)

def test_transfer_fund(driver, config):
    url = config.get('demo', 'url')
    username = config.get('demo', 'username')
    password = config.get('demo', 'password')
    driver.get(url)
    driver.maximize_window()
    time.sleep(10)
    driver.find_element(By.XPATH, "//input[@name='username']").send_keys(username)
    time.sleep(5)
    driver.find_element(By.XPATH, "//input[@name='password']").send_keys(password)
    time.sleep(5)
    driver.find_element(By.XPATH, "//input[@value='Log In']").click()
    time.sleep(10)
    driver.find_element(By.XPATH, "//a[normalize-space()='Transfer Funds']").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//input[@id='amount']").send_keys("1000")
    time.sleep(5)
    driver.find_element(By.XPATH, "//input[@value='Transfer']").click()
    time.sleep(10)


def test_request_loan(driver, config):
    url = config.get('demo', 'url')
    username = config.get('demo', 'username')
    password = config.get('demo', 'password')
    driver.get(url)
    driver.maximize_window()
    time.sleep(10)
    driver.find_element(By.XPATH, "//input[@name='username']").send_keys(username)
    time.sleep(5)
    driver.find_element(By.XPATH, "//input[@name='password']").send_keys(password)
    time.sleep(5)
    driver.find_element(By.XPATH, "//input[@value='Log In']").click()
    time.sleep(10)
    driver.find_element(By.XPATH, "//a[normalize-space()='Request Loan']").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//input[@id='amount']").send_keys("5000")
    time.sleep(5)
    driver.find_element(By.XPATH, "//input[@id='downPayment']").send_keys("3000")
    time.sleep(5)
    driver.find_element(By.XPATH, "//input[@value='Apply Now']").click()
    time.sleep(10)