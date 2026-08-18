import os
import sys
from sqlalchemy import text

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.database.db import engine

if __name__ == "__main__":
    with engine.connect() as conn:
        result = conn.execute(text("SHOW TABLES;"))
        print("Existing tables in database:")
        for row in result:
            print(row[0])
