import pytest
from api_client import TABLE_IDS

@pytest.mark.parametrize("table_name", ["Lections", "Records", "Teachers", "Students", "Problem_marks", "Metaphors"])
def test_table_accessible(client, table_name):
    response = client.get_records(TABLE_IDS[table_name])
    assert response.status_code == 200

@pytest.mark.parametrize("table_name,expected_min_records", [
    ("Lections", 3),
    ("Records", 1),
    ("Teachers", 1),
    ("Students", 1),
    ("Problem_marks", 1),
    ("Metaphors", 1),
])
def test_table_has_min_records(client, table_name, expected_min_records):
    response = client.get_records(TABLE_IDS[table_name])
    assert response.status_code == 200
    
    data = response.json()
    records = data.get("list", [])
    actual_records = len(records)