from functions.data_aggregator import aggregate_game_data, summarize_game_data

from dotenv import load_dotenv
from os import getenv

def main():
	load_dotenv()
	game_name = getenv('GAME_NAME')
	game_url = getenv('GAME_URL')

	aggregate_game_data(game_name)
	summarize_game_data(game_name)

main()