import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

if __name__ == "__main__":
    try:
        response = client.get("/api/subjects/categories")
        print("Status code:", response.status_code)
        print("Response JSON:", response.json())
    except Exception as e:
        import traceback
        traceback.print_exc()
