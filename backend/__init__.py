

from .wrapper import scraper, scraper_recent, ranker
from newswebsite.settings import PRODUCTION

if PRODUCTION:
    from .database_production import reinit_db, store_to_db, get_from_db, delete_from_db, modify_in_db
else:
    from .database import reinit_db, store_to_db, get_from_db, delete_from_db, modify_in_db

from .database_production import get_users
