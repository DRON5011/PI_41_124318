import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from api_client import NocoDBClient, TABLE_IDS

@pytest.fixture
def client():
    return NocoDBClient(token="h070wPAEcnvRUrqeXswZu-LP7HZqnqZCo5PQudOg")

@pytest.fixture
def table_info(client):
    info = {}
    for table_name, table_id in TABLE_IDS.items():
        response = client.get_records(table_id, limit=1)
        if response.status_code == 200:
            data = response.json()
            if data.get("list"):
                info[table_name] = {
                    "fields": list(data["list"][0].keys()),
                    "sample": data["list"][0]
                }
            else:
                info[table_name] = {"fields": [], "sample": None}
        else:
            info[table_name] = {"fields": [], "sample": None, "error": response.status_code}
    return info