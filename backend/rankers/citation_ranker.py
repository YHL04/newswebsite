

from semanticscholar import SemanticScholar
from scholarly import scholarly


def citation_ranker_semantic_scholar(data, url="https://www.semanticscholar.org/"):
    sch = SemanticScholar()

    for i, d in enumerate(data):
        # if citation_rank data exists continue
        if float(d['citation_rank']) >= 0:
            continue

        authors = d["authors"]

        # get total citations of authors
        citations = 0
        for author in authors:
            try:
                result = sch.search_author(author)[0]
                citations += result['citationCount'] / result['paperCount']

            except Exception as e:
                continue

        d['citation_rank'] = str(citations)
        d['final_rank'] = str(citations)

    return data


def citation_ranker_google_scholar(data):
    """
    Returns the total number of citations of all the authors in the paper
    changes ['citation_rank'] in the dictionary and then returns modified data

    Parameters:
        data (List[dict]): A list of dictionary format detailed in database.py

    Returns:
        data (List[dict]): A list of modified dictionary format detailed in database.py
    """
    for i, d in enumerate(data):
        authors = d["authors"]

        # get total citations of authors
        citations = 0
        for author in authors[0]:
            try:
                search_query = scholarly.search_author(author)
                author_result = next(search_query)
                citations += author_result.citedby
            except StopIteration as e:
                # search came up empty probably
                pass
            except AttributeError as e:
                # no citations or can't find citation number probably
                pass
            except Exception as e:
                print("Can't fetch page.")

        d['citation_rank'] = citations
        d['rank'] = citations

    return data

