import pytest
import json
from api_client import TABLE_IDS

class TestMetaphors:
    def test_metaphors_connection(self, client):
        response = client.get_records(TABLE_IDS["Metaphors"])
        assert response.status_code == 200
        
    def test_metaphors_structure(self, client):
        response = client.get_records(TABLE_IDS["Metaphors"])
        assert response.status_code == 200
        
        data = response.json()
        records = data.get("list", [])
        
        if len(records) == 0:
            pytest.skip("Таблица Metaphors пуста")
        
        metaphor = records[0]
        assert "Id" in metaphor
        
        expected_fields = ["short_name", "desc", "time", "students", "records"]
        found_fields = [f for f in expected_fields if f in metaphor]
        assert len(found_fields) > 0
    
    def test_metaphors_data_quality(self, client):
        response = client.get_records(TABLE_IDS["Metaphors"])
        data = response.json()
        metaphors = data.get("list", [])
        
        if not metaphors:
            pytest.skip("Таблица Metaphors пуста")
        
        short_name_count = 0
        desc_count = 0
        
        for metaphor in metaphors:
            if "short_name" in metaphor and metaphor["short_name"]:
                short_name_count += 1
            if "desc" in metaphor and metaphor["desc"]:
                desc_count += 1
        
        assert short_name_count > 0 or desc_count > 0