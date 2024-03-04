

import threading

from backend import scraper, scraper_recent, ranker, reinit_db, store_to_db, get_from_db, delete_from_db


def scrape(keywords, categories):
    # scrape from arXiv
    for category in categories:
        print("Scraping %s" % category)
        try:
            data = scraper_recent(c=category)
            store_to_db(data)
        except Exception as e:
            print(e)

    # scrape from arXiv
    for keyword in keywords:
        print("Scraping %s" % keyword)
        try:
            data = scraper(query=keyword, max_results=1_000)
            store_to_db(data)
        except Exception as e:
            print(e)


def rank(datas, new_datas):
    datas = [datas[i:i+5] for i in range(0, len(datas), 5)]

    count = 0
    for data in datas:
        print(count)
        try:
            count += 5
            data = ranker(data)
            new_datas.extend(data)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    keywords = ["Artificial Intelligence", "Machine Learning"]
    categories = ["cs.AI", "cs.LG"]

    # scrape(keywords, categories)

    # rank news from database
    datas = get_from_db()
    datas = [datas[i:i+20] for i in range(0, len(datas), 20)]

    i = 0
    while i < len(datas):
        new_data = []
        threads = [threading.Thread(target=rank, args=(data, new_data)) for data in datas[i:i+10]]
        for t in threads:
            t.start()

        for t in threads:
            t.join()

        delete_from_db(new_data)
        store_to_db(new_data)

        i += 10

