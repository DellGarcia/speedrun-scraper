from functions import search_and_save_game_links_for
from functions.stats_scraper import get_stats
from dotenv import load_dotenv


if __name__ == '__main__':
    load_dotenv()

    search_and_save_game_links_for()
    get_stats()

