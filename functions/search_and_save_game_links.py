import csv
import os
from .link_scraper import search_category_links_for, search_modality_links_for, search_composed_modality_links_for
from functions import get_driver


def search_and_save_game_links_for(game_name, game_url):
    category_links = {}
    modality_links = {}
    composed_modality_links = {}

    identified_composed = {}

    driver = get_driver()

    try:
        print('Coletando as URLs (Aguarde alguns segundos)')
        search_category_links_for(game_name, game_url, driver, category_links)
        search_modality_links_for(category_links, driver, modality_links, identified_composed)
        search_composed_modality_links_for(identified_composed, driver, composed_modality_links)

        all_links = {**modality_links, **composed_modality_links}

        destination_folder = f'game_links/{game_name}'

        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        with open(f'{destination_folder}/links.csv', 'w') as w:
            for key in all_links:
                w.write(f'{key},{all_links[key]}\n')
    finally:
        print('Fechando browser')
        driver.quit()


