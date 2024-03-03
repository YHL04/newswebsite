

from backend import scraper, ranker, reinit_db, store_to_db, get_from_db, delete_from_db


if __name__ == "__main__":

    keywords = ["Artificial Intelligence", "Machine Learning"]

    # scrape from arXiv
    for keyword in keywords:
        print("Scraping %s" % keyword)
        data = scraper(query=keyword, max_results=10)
        store_to_db(data)

    # rank news from database
    datas = get_from_db()
    datas = [datas[i:i+5] for i in range(0, len(datas), 5)]

    count = 0
    for data in datas:
        print(count)
        count += 5
        data = ranker(data)
        delete_from_db(data)
        store_to_db(data)

