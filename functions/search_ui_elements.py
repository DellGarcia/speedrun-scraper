import os

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException


def get_element_if_exists(driver: WebDriver, element_name: str, parent_element=None) -> WebElement:
    try:
        if parent_element is not None:
            return parent_element.find_element(By.XPATH, os.getenv(element_name))
        else:
            return driver.find_element(By.XPATH, os.getenv(element_name))
    except NoSuchElementException:
        # print(element_name + ' not exists...')
        return None


def get_elements_if_exists(driver: WebDriver, element_name: str, parent_element=None) -> []:
    try:
        if parent_element is not None:
            return parent_element.find_elements(By.XPATH, os.getenv(element_name))
        else:
            return driver.find_elements(By.XPATH, os.getenv(element_name))
    except NoSuchElementException:
        # print(element_name + ' not exists...')
        return None