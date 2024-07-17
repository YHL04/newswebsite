

from datetime import datetime, timedelta

from backend import scraper, scraper_recent, ranker, reinit_db, store_to_db, get_from_db, delete_from_db


def drop_old():
    """drop data 7 days old and data with final rank less than 5"""
    datas = get_from_db()

    drops = []
    for data in datas:
        # if ((data['like_count'] is None) or (data['like_count'] <= 0)):
        #     drops.append(data)
        if (data['date'] < (datetime.today() - timedelta(days=7)).date() and
                ((data['like_count'] is None) or (data['like_count'] <= 0))):
            drops.append(data)
        # elif 0 <= float(data['final_rank']) < 5:
        #     drops.append(data)

    delete_from_db(drops)


def scrape(keywords, categories):
    # scrape from arXiv
    for keyword in keywords:
        print("Scraping %s" % keyword)
        data = scraper(query=keyword, max_results=1000)
        store_to_db(data)

    # scrape from arXiv
    for category in categories:
        print("Scraping %s" % category)
        data = scraper_recent(c=category)
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

    try:
        drop_old()
        scrape(keywords, categories)
    except Exception as e:
        print(e)

    # rank news from database
    datas = get_from_db()
    datas = [datas[i:i+20] for i in range(0, len(datas), 20)]

    for data in datas:
        new_data = []
        rank(data, new_data)

        try:
            delete_from_db(new_data)
            store_to_db(new_data)
        except Exception as e:
            print(e)

    # i = 0
    # while i < len(datas):
    #     new_data = []
    #     threads = [threading.Thread(target=rank, args=(data, new_data)) for data in datas[i:i+20]]
    #     for t in threads:
    #         t.start()
    #
    #     for t in threads:
    #         t.join()
    #
    #     try:
    #         delete_from_db(new_data)
    #         store_to_db(new_data)
    #     except Exception as e:
    #         pass
    #
    #     i += 20

