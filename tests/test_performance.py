import pytest
import time
from api_client import TABLE_IDS

class TestPerformance:
    def test_response_time_all_tables(self, client):
        for table_name, table_id in TABLE_IDS.items():
            start = time.time()
            response = client.get_records(table_id)
            elapsed = time.time() - start
            
            assert response.status_code == 200
            assert elapsed < 2.0