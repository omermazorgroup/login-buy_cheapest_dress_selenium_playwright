import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import re


chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrom_driver_path = "C:/Users/omerm/AppData/Local/Temp/Temp1_chromedriver_win32.zip/chromedriver.exe"


def login_page_initialize():
    """
    A function that go to login page
    """
    driver = webdriver.Chrome(chrom_driver_path, chrome_options=chrome_options)
    driver.maximize_window()
    driver.get('http://automationpractice.com/index.php')
    driver.find_element(By.CSS_SELECTOR, "a.login").click()
    return driver


def submit_form(driver, email, password):
    """
    A function that fill email input and password input and then submit the form
    :param driver:
    :param email: str
    :param password: str
    """
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "passwd").send_keys(password)
    driver.find_element(By.ID, "SubmitLogin").click()


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
    driver = login_page_initialize()
    try:
        time.sleep(1)
        submit_form(driver, email, password)
        time.sleep(1)
        return text in driver.find_element(By.TAG_NAME, "body").text
    finally:
        driver.close()


def find_cheapest(driver) -> tuple | None:
    """
    A function that find the cheapest product from list of products and return it and its price
    :param driver:
    """
    products = driver.find_elements(By.CLASS_NAME, "product-container")
    prices = driver.find_elements(By.CSS_SELECTOR, "span.product-price")
    time.sleep(1)
    prices_list = []
    for price in prices:
        prices_list.append(re.sub('[^\d\.]', "", price.text))
    prices_list = list(filter(None, prices_list))
    for product in products:
        right_block = product.find_element(By.CLASS_NAME, "right-block")
        content_price = right_block.find_element(By.CLASS_NAME, "content_price")
        price = content_price.find_element(By.CLASS_NAME, "price").text
        price_num = str(price[1:len(price)])
        if min(prices_list) == price_num:
            return product, min(prices_list)
    return None


