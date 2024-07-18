

import arxiv


client = arxiv.Client()


"""
Search arXiv in real time and store into database before displaying it to users so that users can like it
and keep it in the database.
"""


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

