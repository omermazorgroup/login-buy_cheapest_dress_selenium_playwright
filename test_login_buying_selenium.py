from threading import Event
import re
from login_buying_selenium import validate_input, login_page_initialize, submit_form, find_cheapest
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import logging
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.ERROR)
mylogger = logging.getLogger()


@pytest.fixture
def user():
    return {
      "email": "omermazor144@gmail.com",
      "password": "12345"
    }


def test_no_email(user):
    mylogger.info("test for empty email input")
    assert validate_input("", user["password"], "An email address required")
    mylogger.info("text succeeded!")


def test_fake_email(user):
    mylogger.info("test for invalid email input")
    assert validate_input("omermazor144@gmail", user["password"], "Invalid email address")
    mylogger.info("text succeeded!")


def test_no_password(user):
    mylogger.info("test for empty password input")
    assert validate_input(user["email"], "", "Password is required")
    mylogger.info("text succeeded!")


def test_invalid_password(user):
    mylogger.info("test for invalid password input")
    assert validate_input(user["email"], "1234", "Invalid password")
    mylogger.info("text succeeded!")


def test_fake_authentication():
    mylogger.info("test for unregistered input")
    assert validate_input("omermazor144@gmail.com", "123456", "Authentication failed")
    mylogger.info("text succeeded!")


def test_valid_authentication(user):
    mylogger.info("test for registered user")
    assert validate_input(user["email"], user["password"], "Welcome to your account")
    mylogger.info("text succeeded!")


def test_click_forgot_password():
    mylogger.info("test for click on forgot password button")
    driver = login_page_initialize()
    time.sleep(2)
    driver.find_element(By.XPATH, '//a[text()="Forgot your password?"]').click()
    time.sleep(2)
    assert driver.current_url == "http://automationpractice.com/index.php?controller=password"
    mylogger.info("text succeeded!")
    driver.close()


def test_buy_cheapest_summer_dress(user):
    mylogger.info("test for buying a cheapest summer dress process")
    driver = login_page_initialize()
    actions = ActionChains(driver)
    time.sleep(1)
    submit_form(driver, user["email"], user["password"])
    time.sleep(1)
    mylogger.info("login to registered account")
    assert "Welcome to your account" in driver.find_element(By.TAG_NAME, "body").text
    driver.find_element(By.ID, "search_query_top").send_keys("summer")
    driver.find_element(By.CSS_SELECTOR, 'button.button-search').click()
    header = driver.find_element(By.CSS_SELECTOR, "#center_column>h1")
    mylogger.info("search for summer dress")
    assert "SUMMER" in header.text
    cheapest, price = find_cheapest(driver)
    time.sleep(2)
    actions.move_to_element(cheapest).perform()
    cheapest.find_element(By.CSS_SELECTOR, 'a.ajax_add_to_cart_button').click()
    time.sleep(10)
    driver.find_element(By.CSS_SELECTOR,
                        "#layer_cart > div.clearfix > div.layer_cart_cart > div.button-container > a").click()
    time.sleep(1)
    driver.find_element(By.CLASS_NAME, "standard-checkout").click()
    driver.find_element(By.CSS_SELECTOR, '[name=processAddress]').click()
    driver.find_element(By.CSS_SELECTOR, 'input#cgv').click()
    driver.find_element(By.CSS_SELECTOR, '[name=processCarrier]').click()
    total_price = driver.find_element(By.ID, "total_product").text
    mylogger.info("check the price of the product")
    assert price == re.sub('[^\d\.]', "", total_price)
    driver.find_element(By.CLASS_NAME, "bankwire").click()
    driver.find_element(By.CSS_SELECTOR, "#cart_navigation > button").click()
    time.sleep(2)
    assert "Your order on My Store is complete" in driver.find_element(By.TAG_NAME, 'body').text
    mylogger.info("text succeeded!")
    driver.close()
