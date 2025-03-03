from link_maker import search_duckduckgo
from scrappers.imdb import scrape_imdb
from scrappers.wiki import scrape_wikipedia
from scrappers.mdl import scrape_mydramalist
from scrappers.mal import scrape_myanimelist
import config
import threading

from datetime import datetime

def start_search(name):
    print(f"Intiating search for {name}...")
    links = search_duckduckgo(name)

    t1 = threading.Thread(target=scrape_imdb(links["IMDb"]))
    t2 = threading.Thread(target=scrape_wikipedia(links["Wikipedia"]))
    t3 = threading.Thread(target=scrape_mydramalist(links["MyDramaList"]))
    t4 = threading.Thread(target=scrape_myanimelist(links["MyAnimeList"]))

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()

    print(config.RESULT)

if __name__ == "__main__":
    start = datetime.now()

    name = input("Enter name: ")
    links = search_duckduckgo(name)

    t1 = threading.Thread(target=scrape_imdb(links["IMDb"]))
    t2 = threading.Thread(target=scrape_wikipedia(links["Wikipedia"]))
    t3 = threading.Thread(target=scrape_mydramalist(links["MyDramaList"]))
    t4 = threading.Thread(target=scrape_myanimelist(links["MyAnimeList"]))

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()

    end = datetime.now()

    print(end-start)

    print(config.RESULT)
