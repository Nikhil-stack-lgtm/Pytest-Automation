import os
import time
from configparser import ConfigParser
from time import sleep

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager


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


def test_login_logout(driver, config):
    # Retrieve URL from config
    url = config.get('detail', 'saucelaburl')
    username = config.get('detail', 'saucelabusername')
    password = config.get('detail', 'saucelabpassword')
    driver.get(url)
    time.sleep(5)
    driver.maximize_window()

    # Input organization ID
    driver.find_element(By.XPATH, "//input[@id='user-name']").send_keys(username)
    driver.find_element(By.XPATH, "//input[@id='password']").send_keys(password)
    driver.find_element(By.XPATH, "//input[@id='login-button']").click()
    sleep(5)
    driver.find_element(By.XPATH, "//button[@id='react-burger-menu-btn']").click()
    driver.implicitly_wait(10)
    driver.find_element(By.XPATH, "//a[@id='logout_sidebar_link']").click()
    sleep(5)


def test_about(driver, config):
    # Retrieve URL from config
    url = config.get('detail', 'saucelaburl')
    username = config.get('detail', 'saucelabusername')
    password = config.get('detail', 'saucelabpassword')
    driver.get(url)
    time.sleep(5)
    driver.maximize_window()

    # Input organization ID
    driver.find_element(By.XPATH, "//input[@id='user-name']").send_keys(username)
    driver.find_element(By.XPATH, "//input[@id='password']").send_keys(password)
    driver.find_element(By.XPATH, "//input[@id='login-button']").click()
    sleep(5)
    driver.find_element(By.XPATH, "//button[@id='react-burger-menu-btn']").click()
    driver.implicitly_wait(10)
    driver.find_element(By.XPATH, "//a[@id='about_sidebar_link']").click()
    sleep(10)


def test_filer(driver, config):
    # Retrieve URL from config
    url = config.get('detail', 'saucelaburl')
    username = config.get('detail', 'saucelabusername')
    password = config.get('detail', 'saucelabpassword')
    driver.get(url)
    time.sleep(5)
    driver.maximize_window()

    # Input organization ID
    driver.find_element(By.XPATH, "//input[@id='user-name']").send_keys(username)
    driver.find_element(By.XPATH, "//input[@id='password']").send_keys(password)
    driver.find_element(By.XPATH, "//input[@id='login-button']").click()
    sleep(5)

    dropdown = Select(driver.find_element("xpath", "//select[@class='product_sort_container']"))
    dropdown.select_by_visible_text("Name (Z to A)")
    # driver.find_element(By.XPATH, "//select[@class='product_sort_container']").click()
    sleep(5)


def test_add_to_cart(driver, config):
    # Retrieve URL from config
    url = config.get('detail', 'saucelaburl')
    username = config.get('detail', 'saucelabusername')
    password = config.get('detail', 'saucelabpassword')
    driver.get(url)
    time.sleep(5)
    driver.maximize_window()

    # Input organization ID
    driver.find_element(By.XPATH, "//input[@id='user-name']").send_keys(username)
    driver.find_element(By.XPATH, "//input[@id='password']").send_keys(password)
    driver.find_element(By.XPATH, "//input[@id='login-button']").click()
    sleep(5)
    driver.find_element(By.XPATH, "//div[normalize-space()='Sauce Labs Backpack']").click()
    sleep(5)
    driver.find_element(By.XPATH, "//button[@id='add-to-cart']").click()
    sleep(5)
    driver.find_element(By.XPATH, "//a[@class='shopping_cart_link']").click()
    sleep(5)
    driver.find_element(By.XPATH, "//button[@id='checkout']").click()
    sleep(5)
    driver.find_element(By.XPATH, "//input[@id='first-name']").send_keys("XYZ")
    driver.find_element(By.XPATH, "//input[@id='last-name']").send_keys("XYZ")
    driver.find_element(By.XPATH, "//input[@id='postal-code']").send_keys("123456")
    driver.find_element(By.XPATH, "//input[@id='continue']").click()
    sleep(5)
    # Take a screenshot after completing the steps
    screenshot_path = os.path.join(os.getcwd(), "screenshot.png")
    driver.save_screenshot(screenshot_path)
    print(f"Screenshot saved at: {screenshot_path}")

    #Finish the operation
    driver.find_element(By.XPATH, "//button[@id='finish']").click()
    sleep(5)
    driver.find_element(By.XPATH, "//button[@id='back-to-products']").click()
    sleep(5)

