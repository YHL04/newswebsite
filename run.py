

import threading
from datetime import datetime, timedelta

from backend import scraper, scraper_recent, ranker, reinit_db, store_to_db, get_from_db, delete_from_db


def drop_old():
    """drop data 14 days old and data with final rank less than 5"""
    datas = get_from_db()

    drops = []
    for data in datas:
        if datetime.strptime(data['date'].split()[0], "%Y-%m-%d") < (datetime.today() - timedelta(days=14)):
            drops.append(data)
        elif 0 <= float(data['final_rank']) < 5:
            drops.append(data)

    delete_from_db(drops)


def scrape(keywords, categories):
    # scrape from arXiv
    for category in categories:
        print("Scraping %s" % category)
        data = scraper_recent(c=category)
        store_to_db(data)

    # scrape from arXiv
    for keyword in keywords:
        print("Scraping %s" % keyword)
        data = scraper(query=keyword, max_results=500)
        store_to_db(data)


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

    scrape(keywords, categories)
    drop_old()

    # rank news from database
    datas = get_from_db()
    datas = [datas[i:i+20] for i in range(0, len(datas), 20)]

    i = 0
    while i < len(datas):
        new_data = []
        threads = [threading.Thread(target=rank, args=(data, new_data)) for data in datas[i:i+20]]
        for t in threads:
            t.start()

        for t in threads:
            t.join()

        delete_from_db(new_data)
        store_to_db(new_data)

        i += 20

