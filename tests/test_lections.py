import pytest
import json
from api_client import TABLE_IDS

class TestProjects:
    def test_lections_connection(self, client):
        response = client.get_records(TABLE_IDS["Lections"])
        assert response.status_code == 200
        
    def test_lections_structure(self, client):
        response = client.get_records(TABLE_IDS["Lections"])
        assert response.status_code == 200
        
        data = response.json()
        lections = data.get("list", [])
        
        if not lections:
            pytest.skip("Таблица Lections пуста")
        
        lection = lections[0]
        assert "Id" in lection
        
        descriptive_fields = ["lection_name", "course_name", "lection_date", "start_time", "end_time", "status", "records", "teachers", "fio (from Teachers)"]
        found_descriptive = [f for f in descriptive_fields if f in lections]
    
    def test_lections_required_fields(self, client):
        response = client.get_records(TABLE_IDS["Lections"])
        data = response.json()
        lections = data.get("list", [])
        
        if not lections:
            pytest.skip("Таблица Lections пуста")
        
        for lection in lections:
            assert "Id" in lection