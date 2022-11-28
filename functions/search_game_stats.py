import os
import re
import time

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException

navigation_memo = []


def search_game_stats_for(driver: WebDriver, destination_folder: str, url: str, page):
    destiny = f'{url}&page={page}'

    if destiny in navigation_memo:
        return

    navigation_memo.append(destiny)

    driver.get(destiny)

    if page > 1:
        time.sleep(0.5)
        page_exists = re.search('&page=', driver.current_url)

        if not page_exists:
            return

    try:
        table = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH, os.getenv('TABLE_ELEMENT')))
        )
    except TimeoutException:
        return

    table_rows = table.find_elements(By.TAG_NAME, 'tr')

    result = ''

    for row in table_rows:
        line = row.text.replace('\n', ',')
        parts = len(line.split(','))

        if parts < 5:
            continue

        cells = row.find_elements(By.TAG_NAME, 'td')

        try:
            player_nationality = cells[1].find_element(By.CLASS_NAME, 'flagicon').get_attribute('alt')
        except NoSuchElementException:
            player_nationality = 'unknown'

        try:
            player_position = cells[0].find_element(By.TAG_NAME, 'img').get_attribute('alt')[0]
            line = f'{player_position},{line},{player_nationality}'
        except NoSuchElementException:
            line = f'{line},{player_nationality}'

        result += line
        result += '\n'

    file_path = f'{destination_folder}/page-{page}.csv'

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    with open(file_path, 'w') as w:
        w.write(result)

    search_game_stats_for(driver, destination_folder, url, page + 1)
