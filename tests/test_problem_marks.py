import pytest
import json
from api_client import TABLE_IDS

class TestProblem_marks:
    def test_problem_marks_connection(self, client):
        response = client.get_records(TABLE_IDS["Problem_marks"])
        assert response.status_code == 200
        
    def test_problem_marks_structure(self, client):
        response = client.get_records(TABLE_IDS["Problem_marks"])
        assert response.status_code == 200
        
        data = response.json()
        problem_marks = data.get("list", [])
        
        if not problem_marks:
            pytest.skip("Таблица Problem_marks пуста")
        
        problem_mark = problem_marks[0]
        assert "Id" in problem_mark
        
        name_fields = ["Name", "name", "Название", "Title"]
        has_name = any(f in problem_mark for f in name_fields)
    
    def test_problem_marks_members_relation(self, client):
        problem_marks_response = client.get_records(TABLE_IDS["Problem_marks"])
        problem_marks_data = problem_marks_response.json()
        problem_marks = problem_marks_data.get("list", [])
        
        if not problem_marks:
            pytest.skip("Нет команд для тестирования")
        
        records_response = client.get_records(TABLE_IDS["Records"])
        records_data = records_response.json()
        records = records_data.get("list", [])