import pytest
import json
from api_client import TABLE_IDS

class TestTeachers:
    def test_teachers_connection(self, client):
        response = client.get_records(TABLE_IDS["Teachers"])
        assert response.status_code == 200
        
    def test_teachers_structure(self, client):
        response = client.get_records(TABLE_IDS["Teachers"])
        assert response.status_code == 200
        
        data = response.json()
        teachers = data.get("list", [])
        
        if not teachers:
            pytest.skip("Таблица Teachers пуста")
        
        teacher = teachers[0]
        assert "Id" in teacher
    
    def test_teachers_grades(self, client):
        response = client.get_records(TABLE_IDS["Teachers"])
        data = response.json()
        teachers = data.get("list", [])
        
        if not teachers:
            pytest.skip("Нет сдач для проверки оценок")
        
        graded = 0
        password_fields = ["password"]
        
        for sub in teachers:
            for field in password_fields:
                if field in sub and sub[field] is not None:
                    graded += 1
                    break