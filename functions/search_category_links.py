import os

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException


def search_category_links_for(game_name: str, game_url: str, driver: WebDriver, collected_links: dict):
    try:
        driver.get(game_url)

        WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH, os.getenv('SHOW_CATEGORIES_BUTTON')))
        ).click()

        categories_el = driver.find_element(By.XPATH, os.getenv('CATEGORY_ELEMENTS'))
        categories_link = categories_el.find_elements(By.TAG_NAME, 'a')

        for link in categories_link:
            text = link.text.replace('/', '-')
            key = f'games/{game_name}/{text}'.strip().replace(' ', '_')
            if key not in collected_links.keys():
                collected_links[key] = link.get_attribute('href')

    except NoSuchElementException:
        print(f'Não foi possivel capturar os links em {game_url}')
