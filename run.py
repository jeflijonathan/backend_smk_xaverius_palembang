import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.database.db import engine, Base
from main import router_instance

if __name__ == "__main__":
    print("Checking and synchronizing database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database synchronization completed!")
    router_instance.listen()
