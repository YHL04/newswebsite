

from datetime import datetime, timedelta

from backend import scraper, scraper_recent, ranker, reinit_db, store_to_db, get_from_db, delete_from_db, modify_in_db
from backend import get_from_stats, store_to_stats, modify_in_stats, delete_from_stats


def drop_old():
    """drop data 7 days old and data with final rank less than 5"""
    datas = get_from_db()

    drops = []
    for data in datas:
        # if ((data['like_count'] is None) or (data['like_count'] <= 0)):
        #     drops.append(data)
        data['like_count'] = 0 if data['like_count'] is None else data['like_count']

        if (data['date'] < (datetime.today() - timedelta(days=7)).date()) and data['like_count'] <= 0:
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


transformers_count = {}
diffusion_count = {}
rl_count = {}
relevance = {}


def get_stats(new_data):
    global transformers_count, diffusion_count, rl_count, relevance

    categories = {"transformer": ["transformer", "llm", "gpt", "tokenizer"],
                  "diffusion": ["diffusion", "ddpm"],
                  "reinforcement": ["reinforcement", "atari"],
                  "other": ["transformer", "llm", "gpt", "tokenizer", "diffusion",
                            "ddpm", "reinforcement", "atari"]}

    for news in new_data:

        relevance[str(news['date'])] = relevance.get(str(news['date']), 0) + float(news['final_rank'])
        for category in categories.keys():
            if any(s in news['text'].lower() for s in categories[category]):
                if category == "transformer":
                    transformers_count[str(news['date'])] = transformers_count.get(str(news['date']), 0) + 1
                if category == "diffusion":
                    diffusion_count[str(news['date'])] = diffusion_count.get(str(news['date']), 0) + 1
                if category == "reinforcement":
                    rl_count[str(news['date'])] = rl_count.get(str(news['date']), 0) + 1


def store_stats():
    global transformers_count, diffusion_count, rl_count, relevance

    dates = transformers_count.keys()
    datas = []
    for date in dates:
        data = {"id": date, "like_count": 0}
        data["transformers_count"] = transformers_count.get(date, 0)
        data["diffusion_count"] = diffusion_count.get(date, 0)
        data["rl_count"] = rl_count.get(date, 0)
        data["relevance"] = relevance.get(date, 0)

        print(data)
        datas.append(data)

    print("deleting")
    delete_from_stats(datas)
    print("storing")
    store_to_stats(datas)


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
        get_stats(new_data)

        try:
            # delete_from_db(new_data)
            # store_to_db(new_data)
            modify_in_db(new_data)
        except Exception as e:
            print(e)

    store_stats()

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

