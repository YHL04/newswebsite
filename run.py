

import argparse

from backend import scraper, scraper_recent, ranker, reinit_db, store_to_db, get_from_db, delete_from_db


if __name__ == "__main__":
    keywords = ["Artificial Intelligence", "Machine Learning"]
    categories = ["cs.AI", "cs.LG"]

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

    # rank news from database
    datas = get_from_db()
    datas = [datas[i:i+5] for i in range(0, len(datas), 5)]

    count = 0
    for data in datas:
        print(count)
        try:
            count += 5
            data = ranker(data)
            delete_from_db(data)
            store_to_db(data)
        except Exception as e:
            print(e)

