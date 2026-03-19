import pytest
import json
from api_client import TABLE_IDS

class Testrecords:
    def test_records_connection(self, client):
        response = client.get_records(TABLE_IDS["Records"])
        assert response.status_code == 200
        
    def test_records_structure(self, client):
        response = client.get_records(TABLE_IDS["Records"], limit=5)
        assert response.status_code == 200
        
        data = response.json()
        records = data.get("list", [])
        
        if not records:
            pytest.skip("Таблица Records пуста")
        
        record = records[0]
        assert "Id" in record
        
        date_fields = ["file_name", "url_audio", "url_texted_audio", "status", "lections", "lection_name", "problem_marks", "metaphors"]
        found_dates = [f for f in date_fields if f in record]
    
    def test_records_with_deadline(self, client):
        response = client.get_records(TABLE_IDS["Records"], limit=20)
        data = response.json()
        records = data.get("list", [])
        
        if not records:
            pytest.skip("Нет задач для проверки")
        
        complete_count = 0
        conspect_count = 0
        uncomplete_count = 0
        date_field1 = "Необработана"
        date_field2 = "Обработана"
        date_field3 = "Конспект"
        
        for record in records:
            if any(field in record for field in date_field1):
                uncomplete_count += 1
            elif any(field in record for field in date_field2):
                uncomplete_count += 1
            elif any(field in record for field in date_field3):
                uncomplete_count += 1    