

from .scrapers import arxiv_scraper, youtube_scraper
from .rankers import citation_ranker_google_scholar, citation_ranker_semantic_scholar

"""
All scrapers have the format:

Parameters:
    query (string): A query
    max_results (int): Max number of results for the scrape
    
Returns:
    results (List[dict]): A list of dictionary containing the scraped content
    
Dictionary:
    {'name', 'date', 'categories', 'authors', 'link', 'text'}

"""


def scraper(query, max_results):
    return arxiv_scraper(query, max_results)


def ranker(data):
    return citation_ranker_semantic_scholar(data)

