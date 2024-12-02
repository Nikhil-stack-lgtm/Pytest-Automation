# import time
#
# import pytest
# import os
# from configparser import ConfigParser
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
#
#
# def read_config():
#     config = ConfigParser()
#     config_file = os.path.join(os.path.dirname(__file__), 'config.ini')
#     print(f"Attempting to read config file at: {config_file}")
#     config.read(config_file)
#     if not config.sections():
#         raise Exception(f"Config file not found or is empty: {config_file}")
#     print(f"Config sections found: {config.sections()}")
#     return config
#
#
# @pytest.fixture(scope="module")
# def driver():
#     # Setup: Initialize the WebDriver
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#     driver.implicitly_wait(10)  # Set implicit wait
#     yield driver
#     driver.quit()  # Teardown: Quit the WebDriver
#
#
# @pytest.fixture(scope="module")
# def config():
#     return read_config()
#
#
# def test_login_logout(driver, config):
#     # Retrieve values from config
#     url = config.get('detail', 'url')
#     orgid = config.get('detail', 'orgid')
#     email = config.get('detail', 'email')
#     password = config.get('detail', 'password')
#
#     # Navigate to the URL
#     driver.get(url)
#
#     # Input organization ID
#     driver.find_element(By.XPATH, "//input[@id='org_id']").send_keys(orgid)
#
#     # Input email
#     driver.find_element(By.XPATH, "//input[@id='email']").send_keys(email)
#
#     # Input password
#     driver.find_element(By.XPATH, "//input[@id='password']").send_keys(password)
#
#     # Click the "Show Password" button
#     driver.find_element(By.XPATH, "//img[@aria-label='Show Password']").click()
#
#     # Click the "Sign In" button
#     driver.find_element(By.XPATH, "//button[normalize-space()='Sign In']").click()
#     time.sleep(15)
#
#     # Click the arrow icon (logout menu)
#     driver.find_element(By.XPATH, "//div[@class='arrow-icon']//*[name()='svg']").click()
#     time.sleep(5)
#
#     # Click the "Sign Out" button
#     driver.find_element(By.XPATH, "//div[@class='sub-menu-card__sign-out']").click()
#     time.sleep(10)
#
#
# def test_login_empty(driver, config):
#     # Retrieve URL from config
#     url = config.get('detail', 'url')
#     driver.get(url)
#
#
#     time.sleep(5)
#     driver.find_element(By.XPATH, "//button[normalize-space()='Sign In']").click()
#     time.sleep(15)
#
#
