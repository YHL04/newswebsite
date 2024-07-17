

import arxiv

import json
import xmltojson
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from datetime import datetime

client = arxiv.Client()


def arxiv_scraper_recent(c="cs.AI"):
    url = "https://arxiv.org/list/{}/pastweek?skip=0&show=1000".format(c)
    url_search = urlopen(url)
    page = url_search.read()

    # get html from beautifulsoup
    html_code = bs(page, "html.parser")

    # load html plaintext into json
    json_code = xmltojson.parse(html_code.prettify())
    json_data = json.loads(json_code)

    json_data = json_data['html']['body']['div'][2]['div']['dl']

    links = []
    titles = []
    authors = []
    categories = []

    for day_data in json_data:
        data1 = day_data['dt']
        data2 = day_data['dd']
        for d1, d2 in zip(data1, data2):
            link = d1['span']['a'][0]['@href']
            links.append(link)

            title = d2['div']['div'][0]['#text']
            title = ' '.join(title.split())
            titles.append(title)

            author = []
            for a in d2['div']['div'][1]['a']:
                try:
                    author.append(a['#text'])
                except Exception as e:
                    pass
            authors.append(author)

            primary_subjects = d2['div']['div'][-1]['span'][-1]['#text'].split('(')[-1]
            primary_subjects = [primary_subjects.split(')')[0]]

            try:
                subjects = d2['div']['div'][-1]['#text']
                if subjects.startswith(';'):
                    subjects = [s.split(')')[0] for s in subjects.split('(')[1:]]
                    primary_subjects.extend(subjects)

            except KeyError as e:
                pass

            categories.append(primary_subjects)

    results = []
    for link, title, author, category in zip(links, titles, authors, categories):
        id = link.split('/')[-1].split('.')
        id = id[0] + id[1]

        link = "https://arxiv.org" + link

        # get html from beautifulsoup
        html_code = bs(urlopen(link).read(), "html.parser")

        # load html plaintext into json
        try:
            json_code = xmltojson.parse(html_code.prettify())
            json_data = json.loads(json_code)
        except Exception as e:
            continue

        # html directory for abstract text
        try:
            text = json_data['html']['body']['div']['main']['div']['div']['div'][0]['div'][2]['div']['blockquote']['#text']
            text = ' '.join(text.split())

            published = json_data['html']['body']['div']['main']['div']['div']['div'][0]['div'][2]['div']['div'][0]['#text']
            published = published[14:-1]
            published = datetime.strptime(published, "%d %b %Y").strftime("%Y-%m-%d")
        except Exception as e:
            continue

        print(title)
        print(published)

        news = {
            'id'           : id,
            'title'        : title,
            'date'         : published,
            'categories'   : category,
            'authors'      : author,
            'link'         : link,
            'text'         : text,
            'affiliations' : "",
            'citation_rank': -1,
            'final_rank'   : -1,
            'likes'        : 0,
            'like_count'   : 0,
        }
        results.append(news)

    return results


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
        published = r.published.strftime('%Y-%m-%d')
        categories = str(r.categories)
        authors = [str(author) for author in r.authors]
        link = str(r.links[0])
        text = str(r.summary)

        print(title)
        print(link)
        print(published)

        news = {
            'id'           : id,
            'title'        : title,
            'date'         : published,
            'categories'   : categories,
            'authors'      : authors,
            'link'         : link,
            'text'         : text,
            'affiliations' : "",
            'citation_rank': -1,
            'final_rank'   : -1,
            'likes'        : 0,
            'like_count'   : 0,
        }

        results.append(news)

    return results


if __name__ == "__main__":
    arxiv_scraper("Machine Learning", 2)
