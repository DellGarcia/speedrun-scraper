import os

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

from functions import get_elements_if_exists, get_element_if_exists
from functions import remove_overlay_for


overlay_problems = ['playBtnStartIcon', 'playBtnStart', 'transparentInner', 'transparentCover', 'adBreakDiv']


def search_modality_links_for(category_links: dict, driver: WebDriver, collected_links: dict, composed_modality: dict):
    for key in category_links:
        driver.get(category_links[key])

        modality_container = WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located((By.XPATH, os.getenv('MODALITY_CONTAINER')))
        )

        if modality_container:
            modality_listbox_button = get_element_if_exists(driver, 'MODALITY_LISTBOX_BUTTON', modality_container)
            modality_radio_group = get_element_if_exists(driver, 'MODALITY_RADIO_GROUP', modality_container)

            if modality_listbox_button and modality_radio_group:
                print(f'Categoria composta encontrada em {key}')
                composed_modality[key] = category_links[key]
                continue

            if modality_listbox_button:
                for item in overlay_problems:
                    remove_overlay_for(driver, item)

                ActionChains(driver).move_to_element(modality_listbox_button).click().perform()

                modality_listbox_options = get_elements_if_exists(driver, 'MODALITY_LISTBOX_OPTIONS', modality_container)

                for link in modality_listbox_options:
                    href = link.get_attribute('href')
                    if href is not None and '(empty)' not in link.text:
                        k = f'{key}/{link.text}'.strip().replace(' ', '_')
                        if k not in collected_links.keys():
                            collected_links[k] = href
            else:
                links = modality_radio_group.find_elements(By.TAG_NAME, 'a')

                for link in links:
                    href = link.get_attribute('href')
                    if href is not None and '(empty)' not in link.text:
                        k = f'{key}/{link.text}'.strip().replace(' ', '_')
                        if k not in collected_links.keys():
                            collected_links[k] = href