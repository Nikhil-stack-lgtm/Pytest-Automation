import configparser
from configparser import ConfigParser
import time
from time import sleep

import pyautogui
import pyperclip
import pytest
# from jsonschema.benchmarks.const_vs_enum import value
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from configparser import ConfigParser
import os


# from seleniumbasicspytest.browser_test import driver

# @pytest.fixture(scope="module")
# def driver():
#     # Setup: Initialize the webdriver
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#     yield driver  # This allows the test to run
#     # Teardown: Close the webdriver
#     driver.quit()

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
    # Load configuration
    # config = ConfigParser()
    # config.read('config.ini')

    # Retrieve URL from config
    url = config.get('detail', 'url')
    orgid = config.get('detail', 'orgid')
    email = config.get('detail', 'email')
    password = config.get('detail', 'password')
    driver.get(url)
    time.sleep(5)

    # Input organization ID
    driver.find_element(By.XPATH, "//input[@id='org_id']").send_keys(orgid)

    # Input email
    driver.find_element(By.XPATH, "//input[@id='email']").send_keys(email)

    # Input password
    driver.find_element(By.XPATH, "//input[@id='password']").send_keys(password)

    # Click the "Show Password" button
    driver.find_element(By.XPATH, "//img[@aria-label='Show Password']").click()

    # Click the "Sign In" button
    driver.find_element(By.XPATH, "//button[normalize-space()='Sign In']").click()
    time.sleep(15)

    # Click the arrow icon (logout menu)
    driver.find_element(By.XPATH, "//div[@class='arrow-icon']//*[name()='svg']").click()
    time.sleep(5)

    # Click the "Sign Out" button
    driver.find_element(By.XPATH, "//div[@class='sub-menu-card__sign-out']").click()
    time.sleep(10)


def test_login_empty(driver, config):
    # Retrieve URL from config
    url = config.get('detail', 'url')
    driver.get(url)
    time.sleep(5)
    driver.find_element(By.XPATH, "//button[normalize-space()='Sign In']").click()
    time.sleep(15)


def test_my_profile(driver, config):
    # Retrieve URL from config
    url = config.get('detail', 'url')
    driver.maximize_window()
    orgid = config.get('detail', 'orgid')
    email = config.get('detail', 'email')
    password = config.get('detail', 'password')
    driver.get(url)
    time.sleep(5)

    # Input organization ID
    driver.find_element(By.XPATH, "//input[@id='org_id']").send_keys(orgid)

    # Input email
    driver.find_element(By.XPATH, "//input[@id='email']").send_keys(email)

    # Input password
    driver.find_element(By.XPATH, "//input[@id='password']").send_keys(password)

    # Click the "Show Password" button
    driver.find_element(By.XPATH, "//img[@aria-label='Show Password']").click()

    # Click the "Sign In" button
    driver.find_element(By.XPATH, "//button[normalize-space()='Sign In']").click()
    time.sleep(15)

    # Navigate to profile settings
    driver.find_element(By.XPATH, "//div[contains(@class,'arrow-icon')]//*[name()='svg']").click()
    driver.find_element(By.XPATH, "//span[normalize-space()='My Profile']").click()
    time.sleep(5)

    # Edit profile
    driver.find_element(By.XPATH, "//button[@class='my-profile__main__user-data__edit-button apply-loader']").click()
    time.sleep(5)

    # Locate fields
    firstname = driver.find_element(By.XPATH, "//input[@id='firstName']")
    lastname = driver.find_element(By.XPATH, "//input[@id='lastName']")
    jobTitle = driver.find_element(By.XPATH, "//input[@id='jobTitle']")

    # Clear existing values using Actions
    actions = ActionChains(driver)
    actions.move_to_element(firstname).double_click().click().send_keys(Keys.BACK_SPACE).perform()
    actions.move_to_element(lastname).double_click().click().send_keys(Keys.BACK_SPACE).perform()
    actions.move_to_element(jobTitle).double_click().click().send_keys(Keys.BACK_SPACE).perform()
    time.sleep(5)

    # Enter new values
    firstname.send_keys("Nikhilesh")
    lastname.send_keys("Nikhilesh")
    jobTitle.send_keys("Nikhilesh")

    # Submit changes
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(10)
    driver.find_element(By.XPATH, "//button[normalize-space()='OKAY']").click()
    time.sleep(5)

    # Edit again and cancel
    driver.find_element(By.XPATH, "//button[@class='my-profile__main__user-data__edit-button apply-loader']").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//button[normalize-space()='Cancel']").click()

    # Logout
    driver.find_element(By.XPATH, "//div[@class='profileWrapper']//*[name()='svg']").click()
    driver.find_element(By.XPATH, "//div[@class='sub-menu-card__sign-out']").click()
    time.sleep(5)


def test_upload_profile_pic(driver, config):
    # Retrieve URL from config
    url = config.get('detail', 'url')
    driver.maximize_window()
    orgid = config.get('detail', 'orgid')
    email = config.get('detail', 'email')
    password = config.get('detail', 'password')
    driver.get(url)
    time.sleep(5)

    # Input organization ID
    driver.find_element(By.XPATH, "//input[@id='org_id']").send_keys(orgid)

    # Input email
    driver.find_element(By.XPATH, "//input[@id='email']").send_keys(email)

    # Input password
    driver.find_element(By.XPATH, "//input[@id='password']").send_keys(password)

    # Click the "Show Password" button
    driver.find_element(By.XPATH, "//img[@aria-label='Show Password']").click()

    # Click the "Sign In" button
    driver.find_element(By.XPATH, "//button[normalize-space()='Sign In']").click()
    time.sleep(15)

    # Navigate to profile settings
    driver.find_element(By.XPATH, "//div[contains(@class,'header-profile-image')]").click()
    driver.find_element(By.XPATH, "//span[normalize-space()='My Profile']").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//div[contains(@class,'cursor-pointer')]").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//button[normalize-space()='Upload']").click()
    time.sleep(5)

    # Set file path to clipboard
    file_path = "C:\\Users\\Admin\\Downloads\\cis-logo.png"
    pyperclip.copy(file_path)

    # Simulate Ctrl+V to paste the file path
    pyautogui.keyDown('ctrl')  # Press Ctrl
    pyautogui.press('v')  # Press V key
    pyautogui.keyUp('ctrl')  # Release Ctrl key

    # Add delay for processing
    time.sleep(10)

    # Simulate pressing Enter
    pyautogui.press('enter')

    # Delay for file upload completion
    time.sleep(10)
    driver.find_element(By.XPATH, "//button[normalize-space()='Save']").click()
    time.sleep(20)

    driver.find_element(By.XPATH, "//button[@id='simple-tab-1']").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//span[@class='owner-permissions-view__link']").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//span[normalize-space()='Team Management']").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//span[normalize-space()='Settings']").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//span[normalize-space()='FAQ']").click()
    time.sleep(5)
    driver.find_element(By.XPATH,
                        "//div[contains(@class,'common-accordion__head__title permissions-accordion__head__title title apply-loader')]//span[contains(@class,'typography__body-3 typography__body-3__medium')][normalize-space()='Submit Feedback']").click()
    time.sleep(5)

    # Remove Photo
    driver.find_element(By.XPATH, "//div[contains(@class,'cursor-pointer')]").click()
    time.sleep(5)
    driver.find_element(By.XPATH,
                        "//button[contains(@class,'upload_container__icon upload_container__icon--delete')]//*[name()='svg']").click()
    time.sleep(10)
    driver.find_element(By.XPATH, "(//img[@alt='close_icon'])[1]").click()
    time.sleep(5)

    # Logout
    driver.find_element(By.XPATH, "//div[@class='profileWrapper']//*[name()='svg']").click()
    driver.find_element(By.XPATH, "//div[@class='sub-menu-card__sign-out']").click()
    time.sleep(5)


def test_settings(driver, config):
    # Load configuration
    # config = ConfigParser()
    # config.read('config.ini')

    # Retrieve URL from config
    url = config.get('detail', 'url')
    driver.maximize_window()
    orgid = config.get('detail', 'orgid')
    email = config.get('detail', 'email')
    password = config.get('detail', 'password')
    orgname = config.get('detail', 'orgname')
    country = config.get('detail', 'country')
    state = config.get('detail', 'state')
    driver.get(url)
    time.sleep(5)

    # Input organization ID
    driver.find_element(By.XPATH, "//input[@id='org_id']").send_keys(orgid)

    # Input email
    driver.find_element(By.XPATH, "//input[@id='email']").send_keys(email)

    # Input password
    driver.find_element(By.XPATH, "//input[@id='password']").send_keys(password)

    # Click the "Show Password" button
    driver.find_element(By.XPATH, "//img[@aria-label='Show Password']").click()

    # Click the "Sign In" button
    driver.find_element(By.XPATH, "//button[normalize-space()='Sign In']").click()
    time.sleep(15)
    driver.find_element(By.XPATH,
                        "//a[contains(@href,'/settings')]//div[contains(@class,'tooltip-custom')]//*[name()='svg']").click()
    time.sleep(15)
    driver.find_element(By.XPATH, "//button[normalize-space()='Edit']").click()
    time.sleep(10)
    driver.find_element(By.XPATH, "//input[@placeholder='Enter Organization Name']").clear()
    time.sleep(5)
    driver.find_element(By.XPATH, "//button[normalize-space()='Cancel']").click()
    time.sleep(10)
    driver.find_element(By.XPATH, "//button[normalize-space()='Edit']").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//input[@placeholder='Enter Organization Name']").clear()
    time.sleep(5)

    xpath = f"//input[@placeholder='Enter Organization Name']"
    driver.find_element(By.XPATH, xpath).send_keys(orgname)
    # driver.find_element(By.XPATH, "//input[@placeholder='Enter Organization Name']").send_keys("nICK oRG")
    # time.sleep(5)
    driver.find_element(By.XPATH, "//input[@id='country']").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//input[@id='country']").clear()
    time.sleep(5)
    # driver.find_element(By.XPATH, "//li[normalize-space()='India']").click()
    xpath = f"//li[normalize-space()='{country}']"
    driver.find_element(By.XPATH, xpath).click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//input[@id='state']").click()
    # time.sleep(5)
    # driver.find_element(By.XPATH, "xpath://input[@id='state']").clear()
    time.sleep(10)
    xpath = f"//li[normalize-space()='{state}']"
    driver.find_element(By.XPATH, xpath).click()
    # time.sleep(5)
    # driver.find_element(By.XPATH, "//li[normalize-space()='Maharashtra']").click()
    time.sleep(10)
    driver.find_element(By.XPATH, "//button[normalize-space()='Save']").click()
    time.sleep(10)
    driver.find_element(By.XPATH, "//button[normalize-space()='OKAY']").click()
    time.sleep(10)

    driver.find_element(By.XPATH, "//button[@id='simple-tab-1']").click()
    time.sleep(5)  # Wait up to 5 seconds
    driver.find_element(By.XPATH,
                        "//div[contains(@class,'protectedLayout__container__bottomNavigationClose')]//div[2]//div[2]//div[2]//div[1]//div[3]//div[1]//span[1]//img[1]").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//p[normalize-space()='05:00 pm']").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//button[normalize-space()='Schedule']").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "(//img[contains(@alt,'Edit')])[3]").click()
    driver.implicitly_wait(5)
    driver.find_element(By.XPATH, "//p[normalize-space()='05:00 pm']").click()
    driver.implicitly_wait(5)
    driver.find_element(By.XPATH, "//button[normalize-space()='Schedule']").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "(//img[contains(@alt,'Edit')])[5]").click()
    driver.implicitly_wait(5)
    driver.find_element(By.XPATH, "//p[normalize-space()='05:00 pm']").click()
    driver.implicitly_wait(5)
    driver.find_element(By.XPATH, "//button[normalize-space()='Schedule']").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "(//img[contains(@alt,'Edit')])[6]").click()
    driver.implicitly_wait(5)
    driver.find_element(By.XPATH, "//p[normalize-space()='05:00 pm']").click()
    driver.implicitly_wait(5)
    driver.find_element(By.XPATH, "//button[normalize-space()='Schedule']").click()
    time.sleep(10)
    driver.find_element(By.XPATH, "//button[@id='simple-tab-2']").click()
    time.sleep(5)

    # Logout
    driver.find_element(By.XPATH, "//div[@class='profileWrapper']//*[name()='svg']").click()
    driver.find_element(By.XPATH, "//div[@class='sub-menu-card__sign-out']").click()
    time.sleep(5)


def test_add_user(driver, config):
    # Load configuration
    # config = ConfigParser()
    # config.read('config.ini')

    # Retrieve URL from config
    url = config.get('detail', 'url')
    driver.maximize_window()
    orgid = config.get('detail', 'orgid')
    email = config.get('detail', 'email')
    password = config.get('detail', 'password')
    adduser = config.get('detail', 'adduser')
    driver.get(url)
    time.sleep(5)

    # Input organization ID
    sleep(10)
    driver.find_element(By.XPATH, "//input[@id='org_id']").send_keys(orgid)

    # Input email
    driver.find_element(By.XPATH, "//input[@id='email']").send_keys(email)

    # Input password
    driver.find_element(By.XPATH, "//input[@id='password']").send_keys(password)

    # Click the "Show Password" button
    driver.find_element(By.XPATH, "//img[@aria-label='Show Password']").click()

    # Click the "Sign In" button
    driver.find_element(By.XPATH, "//button[normalize-space()='Sign In']").click()
    driver.implicitly_wait(15)  # Wait up to 5 seconds
    driver.find_element(By.XPATH, "//a[contains(@href,'/team-management/users')]").click()
    time.sleep(15)
    driver.find_element(By.XPATH, "//button[@class='add-user apply-loader']").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//input[@id='firstName']").send_keys("Nikhil")
    driver.find_element(By.XPATH, "//input[@id='lastName']").send_keys("G")
    time.sleep(5)
    driver.find_element(By.XPATH, "//button[normalize-space()='Next']").click()
    driver.find_element(By.XPATH, "//input[@id='email']").send_keys(adduser)
    driver.find_element(By.XPATH, "//input[@id='jobTitle']").send_keys("SE")
    driver.find_element(By.XPATH, "//button[normalize-space()='Next']").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//input[contains(@value,'Edit Cloud Accounts, Slack, MS Teams, Email')]").click()
    sleep(10)
    driver.find_element(By.XPATH,
                        "//p[contains(@class,'typography__body-3 typography__body-3__medium label')][normalize-space()='Cloud Accounts']").click()
    time.sleep(5)
    driver.find_element(By.XPATH,
                        "//p[contains(@class,'typography__body-3 typography__body-3__medium label')][normalize-space()='Team Management']").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//input[contains(@value,'View Users, teams, archived users')]").click()
    driver.find_element(By.XPATH, "//input[@value='Edit Users, teams, archived users']").click()
    time.sleep(5)
    driver.find_element(By.XPATH,
                        "//p[contains(@class,'typography__body-3 typography__body-3__medium label')][normalize-space()='Team Management']").click()
    time.sleep(5)
    driver.find_element(By.XPATH,
                        "//p[@class='typography__body-3 typography__body-3__medium label'][normalize-space()='Settings']").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//input[contains(@value,'View Organization, Notifications, Account')]").click()
    driver.find_element(By.XPATH,
                        "//input[@value='Edit Organization, Notifications | Edit Account - owner only ']").click()
    time.sleep(5)
    driver.find_element(By.XPATH,
                        "//p[@class='typography__body-3 typography__body-3__medium label'][normalize-space()='Settings']").click()
    time.sleep(5)
    driver.find_element(By.XPATH,
                        "//p[contains(@class,'typography__body-3 typography__body-3__medium label')][normalize-space()='FAQ']").click()
    time.sleep(5)
    driver.find_element(By.XPATH,
                        "//p[contains(@class,'typography__body-3 typography__body-3__medium label')][normalize-space()='FAQ']").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//p[normalize-space()='Submit Feedback']").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//button[normalize-space()='Review']").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//span[normalize-space()='Cloud Accounts']").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//span[contains(text(),'Team Management')]").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//span[contains(text(),'Team Management')]").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//span[normalize-space()='Settings']").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//span[normalize-space()='Settings']").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//button[normalize-space()='Send Invite']").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//button[normalize-space()='OKAY']").click()
    time.sleep(10)
    driver.get("https://yopmail.com/en/")
    time.sleep(5)
    driver.find_element(By.XPATH, "//input[@id='login']").send_keys(adduser)
    time.sleep(10)
    driver.find_element(By.XPATH, "//i[@class='material-icons-outlined f36']").click()
    time.sleep(5)
