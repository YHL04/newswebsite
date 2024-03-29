# A news website for everything AI

This is a website for scraping content related to AI research so that it can be more accessible to researchers.
The goal is to try to make it a source of information by gathering and ranking related work.

## Image

<img src="https://github.com/YHL04/newswebsite/blob/main/img/img.png" alt="drawing" width="600"/>

## Open Source

For development mode on local pc, inside newswebsite/settings.py
```python
PRODUCTION = False
```

Then, run on localhost
```bash
python manage.py runserver
```



## Link to website


www.aipapernews.com


## Resources

django: https://docs.djangoproject.com/en/5.0/intro/tutorial01/

mysql with django: https://help.pythonanywhere.com/pages/UsingMySQL/

pythonanywhere: https://www.pythonanywhere.com/

namecheap: https://www.namecheap.com/


## Ranking algorithm

according to authors, material, grammar, 
number of authors, keywords, novelty, 
sota, results, sentiment analysis?

## Features

- [X] finish main page with button corresponding to each day
- [X] create scraper and ranker with github actions
- [X] create development and production mode
- [X] create a database system with remote MySQL
- [X] host website
- [X] create gmail login
- [X] create like button (requires login)
- [X] added affiliations to papers
- [ ] create comment section? (requires login)
- [ ] try to promote website

