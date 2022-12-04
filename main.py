# from functions import search_and_save_game_links_for
# from functions.stats_scraper import get_stats
from data_agregator import agregate_game_data
from dotenv import load_dotenv


if __name__ == '__main__':
    load_dotenv()

    # search_and_save_game_links_for()
    # get_stats()
    agregate_game_data()


