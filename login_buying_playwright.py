import time
from playwright.sync_api import sync_playwright
from playwright.async_api import Playwright, async_playwright, Page
from threading import Event


def login_page_initialize(playwright) -> Page:
    """
    A function that go to login page
    :param playwright:
    """
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://automationpractice.com/index.php")
    page.locator("a.login").click()
    return page


def submit_form(page, email, password) -> None:
    """
    A function that fill email input and password input and then submit the form
    :param page:
    :param email: str
    :param password: str
    """
    page.locator("input#email").fill(email)
    page.locator("input#passwd").fill(password)
    page.locator("#SubmitLogin").click()


def validate_input(email: str = None, password: str = None, text: str = None) -> bool:
    """
    A function that enters the login page, fill the email input and
    password input and then submit the form, its return true if the text which is entered
    as a parameter appears in the page after submitted the form.
    :param email: str
    :param password: str
    :param text: str
    :return: bool, True if text parameter is appears in the page after submitted the form, False if not
    """
    if not isinstance(email, str):
        raise TypeError("email must be a string!")
    if not isinstance(password, str):
        raise TypeError("password must be a string!")
    with sync_playwright() as playwright:
        page = login_page_initialize(playwright)
        time.sleep(2)
        submit_form(page, email, password)
        time.sleep(2)
        return text in page.locator('body').inner_html()
        # Event().wait()



