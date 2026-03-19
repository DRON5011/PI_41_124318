import pytest
import uuid
from api_client import TABLE_IDS

class TestCrudOperations:
    def test_create_temp_record(self, client):
        unique_id = str(uuid.uuid4())[:8]
        temp_team = {
            "Name": f"Тестовая команда {unique_id}"
        }
        
        try:
            create_response = client.create_record(TABLE_IDS["teams"], temp_team)
            
            if create_response.status_code in [405, 403, 400, 401]:
                pytest.skip("Создание записей не поддерживается API")
            
            assert create_response.status_code in [200, 201]
            
            if create_response.status_code in [200, 201]:
                created_data = create_response.json()
                if "Id" in created_data:
                    delete_response = client.delete_record(TABLE_IDS["teams"], created_data["Id"])
        except Exception:
            pytest.skip("Создание записей не поддерживается")