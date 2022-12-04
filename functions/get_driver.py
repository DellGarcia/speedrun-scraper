from selenium import webdriver

from selenium.webdriver.firefox.webdriver import WebDriver
from webdriver_manager.firefox import GeckoDriverManager

executable_path = GeckoDriverManager().install()


def get_driver() -> WebDriver:
    from selenium.webdriver.firefox.options import Options

    options = Options()

    return webdriver.Firefox(options=options, executable_path=executable_path)
