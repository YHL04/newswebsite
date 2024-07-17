

from semanticscholar import SemanticScholar
from scholarly import scholarly


def citation_ranker_semantic_scholar(data):
    sch = SemanticScholar()

    for i, d in enumerate(data):
        # if citation_rank data exists continue
        if float(d['citation_rank']) > 0:
            continue

        authors = d["authors"]

        # rank = ( summation( citation+(i == 0)*citation*2 ) / (num_authors+2) ) * num_authors**(1/3)
        citations, final, num_authors = 0, 0, 0
        affiliations = []
        for i, author in enumerate(authors):
            try:
                result = sch.search_author(author)[0]

                # get affiliations
                affiliations += result['affiliations']

                # get citations
                citation = result['citationCount'] / result['paperCount']
                citations += citation

                # if first author, multiply by 3
                final += citation + int(i == 0) * citation * 2
                num_authors += 1

            except Exception as e:
                continue

        if num_authors == 0:
            final = 1
        else:
            final = (final / (num_authors+2)) * (num_authors**(1/3))

        citations = round(citations, 2)
        final = round(final, 2)

        d['affiliations'] = ', '.join(list(set(affiliations)))
        d['citation_rank'] = str(citations)
        d['final_rank'] = str(final)
        d['likes'] = int(0)
        print(d['affiliations'])

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


if __name__ == "__main__":
    citation_ranker_semantic_scholar()