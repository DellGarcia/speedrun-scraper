import threading

from functions import get_driver
from functions import search_game_stats_for

from dotenv import load_dotenv
from os import getenv

load_dotenv()

num_threads = int(getenv('NUM_THREADS'))
drivers = []
threads_payload = {}


def get_stats(game_name):
    with open(f'game_links/{game_name}/links.csv', 'r') as r:
        file_text = r.read()

    lines = file_text.split('\n')

    urls = {}

    for line in lines:
        parts = line.strip().split(',')

        if len(parts) != 2:
            continue

        urls[parts[0]] = parts[1]

    for _ in range(num_threads):
        drivers.append(get_driver())

    index = 0
    for key in urls:
        work = (key, urls[key])

        i = index % num_threads
        if i not in threads_payload.keys():
            threads_payload[i] = [work]
        else:
            threads_payload[i].append(work)

        index += 1

    for i in range(num_threads):
        thread = threading.Thread(target=status_scraper_thread, args=(i,))
        thread.start()


def status_scraper_thread(thread_id):
    try:
        while len(threads_payload[thread_id]) > 0:
            folder, url = threads_payload[thread_id].pop()
            print(f'Thread {thread_id} processando {url}')

            search_game_stats_for(drivers[thread_id], folder, url, 1)
    finally:
        print(f'Acabou o serviço na thread {thread_id}')
        drivers[thread_id].quit()
