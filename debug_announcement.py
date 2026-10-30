import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.database.db import get_db
from domains.announcement.announcement_repository import AnnouncementRepository

db = next(get_db())
repo = AnnouncementRepository()

try:
    results = repo.find_all(db, paginator={"page": 1, "limit": 10})
    print("SUCCESS! Got", len(results), "results")
    for r in results:
        print(r.__dict__)
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
