import os
import sys
from sqlalchemy import text

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.database.db import engine

with engine.begin() as conn:
    try:
        conn.execute(text("ALTER TABLE users ADD COLUMN nomor_telepon VARCHAR(20) UNIQUE;"))
        print("Successfully added 'nomor_telepon' column to 'users' table.")
    except Exception as e:
        print(f"Error altering table: {e}")
