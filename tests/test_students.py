import pytest
import json
from api_client import TABLE_IDS

class TestStudents:
    def test_students_connection(self, client):
        response = client.get_records(TABLE_IDS["Students"])
        assert response.status_code == 200
        
    def test_students_structure(self, client):
        response = client.get_records(TABLE_IDS["Students"])
        assert response.status_code == 200
        
        data = response.json()
        students = data.get("list", [])
        
        if not students:
            pytest.skip("Таблица Students пуста")
        
        student = students[0]
        assert "Id" in student
    
    def test_students_fio(self, client):
        response = client.get_records(TABLE_IDS["Students"])
        data = response.json()
        students = data.get("list", [])
        
        if not students:
            pytest.skip("Нет участников для проверки ролей")
        
        role_fields = ["fio"]
        for student in students[:5]:
            for field in role_fields:
                if field in student:
                    break