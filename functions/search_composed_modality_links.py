import os

from selenium import webdriver

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

from functions import get_elements_if_exists, get_element_if_exists
from functions import remove_overlay_for

overlay_problems = ['playBtnStartIcon', 'playBtnStart', 'transparentInner', 'transparentCover', 'adBreakDiv']


def search_composed_modality_links_for(composed_links: dict, driver: WebDriver, collected_links: dict):
    for key in composed_links:
        driver.get(composed_links[key])

        modality_container = WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located((By.XPATH, os.getenv('MODALITY_CONTAINER')))
        )

        modality_listbox_button = get_element_if_exists(driver, 'MODALITY_LISTBOX_BUTTON', modality_container)

        for item in overlay_problems:
            remove_overlay_for(driver, item)

        ActionChains(driver).move_to_element(modality_listbox_button).click().perform()

        modality_listbox_options = get_elements_if_exists(driver, 'MODALITY_LISTBOX_OPTIONS', modality_container)

        links = {}
        for link in modality_listbox_options:
            href = link.get_attribute('href')
            if href is not None and '(empty)' not in link.text:
                text = link.text.replace('/', '-')
                links[text] = href

        for link in links:
            driver.get(links[link])

            modality_container = WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((By.XPATH, os.getenv('MODALITY_CONTAINER')))
            )

            modality_radio_group = get_element_if_exists(driver, 'MODALITY_RADIO_GROUP', modality_container)

            modality_links = modality_radio_group.find_elements(By.TAG_NAME, 'a')

            for final_link in modality_links:
                href = final_link.get_attribute('href')
                if href is not None and '(empty)' not in final_link.text:
                    link_text = link.replace('/', '-')
                    sub_link_text = final_link.text.replace('/', '-')
                    k = f'{key}/{link_text}/{sub_link_text}'.strip().replace(' ', '_')
                    if k not in collected_links.keys():
                        collected_links[k] = href
