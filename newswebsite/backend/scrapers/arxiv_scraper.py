

import arxiv

import re
import json
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen

client = arxiv.Client()


# def arxiv_category_scraper():
#     scraper = Scraper(category='cs', date_from='2024-02-05', date_until='2024-12-30')
#     # scraper = scraper.scrape_text('arxiv')
#     sent_cnts = scraper.scrape_text('arxiv', save_to=['class1.txt', 'class2.txt'], log_to='test.log')
#     print(sent_cnts)
#     return scraper


def arxiv_recent_scraper():
    url = "https://arxiv.org/list/cs.AI/pastweek?skip=0&show=1000"
    url_search = urlopen(url)
    page = url_search.read()

    html_code = bs(page, "html.parser")
    print(html_code)

    # pattern = r'<script nonce="[-\w]+">\n\s+var ytInitialData = (.+)'
    # script_data = re.search(pattern=pattern, string=html_code.prettify())[1].replace(';', '')

    # Load the JSON data into a Python dictionary
    # json_data = json.loads(script_data)
    # print(json_data)


def arxiv_scraper(query, max_results):
    """
    variables of r in client.results(search):

    title: title of the paper
    doi:
    categories,
    comment,
    entry_id,
    journal_ref,
    primary_category,
    updated

    """

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    results = []
    for r in client.results(search):
        id = str(r.entry_id[-12:-8]) + str(r.entry_id[-7:-2])
        title = str(r.title)
        published = str(r.published)
        categories = str(r.categories)
        authors = [str(author) for author in r.authors]
        link = str(r.links[0])
        text = str(r.summary)

        print(title)
        print(published)

        news = {
            'id'           : id,
            'title'        : title,
            'date'         : published,
            'categories'   : categories,
            'authors'      : authors,
            'link'         : link,
            'text'         : text,
            'citation_rank': -1,
            'rank'         : -1,
            'likes'        : 0,
        }

        results.append(news)

    return results


if __name__ == "__main__":
    arxiv_scraper("Artificial Intelligence", 2)
    arxiv_scraper("Machine Learning", 2)
    # arxiv_category_scraper()

