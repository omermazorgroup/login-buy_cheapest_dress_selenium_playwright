from playwright.sync_api import sync_playwright
from login_buying_playwright import validate_input, login_page_initialize, submit_form
import time
import re
import pytest
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
    with sync_playwright() as playwright:
        page = login_page_initialize(playwright)
        time.sleep(2)
        page.locator('text=Forgot your password?').click()
        time.sleep(2)
        assert page.url == "http://automationpractice.com/index.php?controller=password"
    mylogger.info("text succeeded!")


def test_buy_cheapest_summer_dress(user):
    mylogger.info("test for buying a cheapest summer dress process")
    with sync_playwright() as playwright:
        page = login_page_initialize(playwright)
        time.sleep(2)
        submit_form(page, user["email"], user["password"])
        time.sleep(2)
        mylogger.info("login to registered account")
        assert "Welcome to your account" in page.locator("body").inner_html()
        page.locator('#search_query_top').fill('summer')
        page.locator('button.button-search').click()
        header = page.locator("h1.page-heading:has-text('SUMMER')")
        mylogger.info("search for summer dress")
        assert "summer" in header.inner_html()
        products = page.locator('ul.product_list li')
        prices = page.locator('ul.product_list li .product-price')
        time.sleep(2)
        prices_list = []
        for price in prices.all_inner_texts():
            prices_list.append(re.sub('[^\d\.]', "", price))
        cheapest = products.locator(f".product-container:has-text('${(min(prices_list))}')")
        cheapest.hover()
        page.wait_for_timeout(3000)
        cheapest.locator("text='Add to cart'").click()
        page.locator("text='Proceed to checkout'").click()
        time.sleep(2)
        page.locator("#center_column >> text='Proceed to checkout'").click()
        page.locator("button >> text='Proceed to checkout'").click()
        page.locator("input#cgv").click()
        page.locator("button >> text='Proceed to checkout'").click()
        total_price = page.locator("#total_product").inner_text()
        mylogger.info("check the price of the product")
        assert min(prices_list) == re.sub('[^\d\.]', "", total_price)
        page.locator("text='Pay by bank wire'").click()
        page.locator("button >> text='I confirm my order'").click()
        time.sleep(1)
        assert "Your order on My Store is complete" in page.locator('body').inner_html()
        mylogger.info("text succeeded!")
    # Event().wait()

