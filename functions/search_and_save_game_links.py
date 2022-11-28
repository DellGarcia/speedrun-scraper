from functions import search_category_links_for
from functions import search_modality_links_for
from functions import search_composed_modality_links_for
from functions import get_driver


def search_and_save_game_links_for():
    category_links = {}
    modality_links = {}
    composed_modality_links = {}

    all_links = {}

    identified_composed = {}

    driver = get_driver()

    try:
        print('Coletando as URLs (Aguarde alguns segundos)')
        search_category_links_for('Hollow Knight', 'https://www.speedrun.com/hollowknight', driver, category_links)
        search_modality_links_for(category_links, driver, modality_links, identified_composed)
        search_composed_modality_links_for(identified_composed, driver, composed_modality_links)

        all_links = {**modality_links, **composed_modality_links}
    except Exception as ex:
        print(ex)
    finally:
        print('Fechando browser')
        driver.quit()

    with open('links.csv', 'w') as w:
        for key in all_links:
            w.write(f'{key},{all_links[key]}\n')
