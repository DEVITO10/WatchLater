
from duckduckgo_search import DDGS

def search_duckduckgo(name):
    query_imdb = f"{name} site:imdb.com/title"
    query_wiki = f"{name} site:en.wikipedia.org"
    query_mdl = f"{name} site:mydramalist.com"
    query_mal = f"{name} site:myanimelist.net/anime"
    
    results = []

    # fetching search results
    with DDGS(proxy="tb", timeout=20) as ddgs:
        results.extend(list(ddgs.text(query_imdb, max_results=5)))

    with DDGS(proxy="tb", timeout=20) as ddgs:
        results.extend(list(ddgs.text(query_wiki, max_results=5)))

    with DDGS(proxy="tb", timeout=20) as ddgs:
        results.extend(list(ddgs.text(query_mdl, max_results=5)))

    with DDGS(proxy="tb", timeout=20) as ddgs:
        results.extend(list(ddgs.text(query_mal, max_results=5)))

    links = {"IMDb": None, "Wikipedia": None, "MyDramaList": None, "MyAnimeList": None}

    # keeping only the first link of every website
    for result in results:
        url = result["href"]
        if "imdb.com" in url and not links["IMDb"]:
            links["IMDb"] = url
            break
    
    for result in results:
        url = result["href"]
        if "en.wikipedia.org" in url and not links["Wikipedia"]:
            links["Wikipedia"] = url
            break

    for result in results:
        url = result["href"]
        if "mydramalist.com" in url and not links["MyDramaList"]:
            links["MyDramaList"] = url
            break

    for result in results:
        if (result['href'])[-6:] != "/video":
            url = result["href"]
            if "myanimelist.net" in url and not links["MyAnimeList"]:
                links["MyAnimeList"] = url
                break
        else:
            continue

    return links