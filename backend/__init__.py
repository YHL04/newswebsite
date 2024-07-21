

from .wrapper import scraper, scraper_recent, ranker
from newswebsite.settings import PRODUCTION

if PRODUCTION:
    from .database_production import (reinit_db, store_to_db, get_from_db, delete_from_db, modify_in_db,
                                      get_from_stats, store_to_stats, modify_in_stats, delete_from_stats)
else:
    from .database import (reinit_db, store_to_db, get_from_db, delete_from_db, modify_in_db,
                           get_from_stats, store_to_stats, modify_in_stats, delete_from_stats)

from .database_production import get_users
