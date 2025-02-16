from links import search_duckduckgo
from scrappers.imdb import scrape_imdb
from scrappers.wiki import scrape_wikipedia
from scrappers.mdl import scrape_mydramalist
from scrappers.mal import scrape_myanimelist

if __name__ == "__main__":
    name = input("Enter name: ")
    links = search_duckduckgo(name)

    print("\nIMDb Data:")
    print(scrape_imdb(links["IMDb"]))

    print("\nWikipedia Data:")
    print(scrape_wikipedia(links["Wikipedia"]))

    print("\nMyDramaList Data:")
    print(scrape_mydramalist(links["MyDramaList"]))

    print("\nMyAnimeList Data:")
    print(scrape_myanimelist(links["MyAnimeList"]))
