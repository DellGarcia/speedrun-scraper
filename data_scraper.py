from functions import search_and_save_game_links_for
from functions.stats_scraper import get_stats
from dotenv import load_dotenv
from os import getenv


if __name__ == '__main__':
    load_dotenv()

    game_name = getenv('GAME_NAME')
    game_url = getenv('GAME_URL')

    search_and_save_game_links_for(game_name, game_url)
    get_stats(game_name)
    

