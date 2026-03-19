import requests
from typing import Dict, List, Optional, Any

TABLE_IDS = {
    'Lections': 'm4i2yylgaqvy4m5',
    'Records': 'mxiqj9yx82ds334',
    'Teachers': 'm0s0n53zz8856sk',
    'Students': 'mxwx2ut83p8ft5c',
    'Problem_marks': 'mfjndhoxhp3hols',
    'Metaphors': 'mtzlwx9b3m6cz9b',
}

class NocoDBClient:
    """Клиент для работы с NocoDB API v2"""
    
    def __init__(self, base_url: str = "http://localhost:8080", token: str = ""):
        self.base_url = base_url.rstrip('/')
        self.token = token
        self.headers = {'xc-token': token} if token else {}
    
    def get_records(self, table_id: str, params: Optional[Dict] = None) -> requests.Response:
        """
        Получить записи из таблицы.
        Возвращает Response объект для проверки статуса.
        """
        url = f"{self.base_url}/api/v2/tables/{table_id}/records"
        default_params = {"limit": 100}
        if params:
            default_params.update(params)
        
        response = requests.get(url, headers=self.headers, params=default_params)
        return response
    
    def get_records_json(self, table_id: str, params: Optional[Dict] = None) -> List[Dict]:
        """
        Получить записи и вернуть как JSON.
        """
        response = self.get_records(table_id, params)
        response.raise_for_status()
        data = response.json()
        return data.get('list', []) if isinstance(data, dict) else data
    
    def create_record(self, table_id: str, data: Dict) -> requests.Response:
        """Создать новую запись"""
        url = f"{self.base_url}/api/v2/tables/{table_id}/records"
        response = requests.post(url, headers=self.headers, json=data)
        return response
    
    def update_record(self, table_id: str, record_id: str, data: Dict) -> requests.Response:
        """Обновить запись"""
        url = f"{self.base_url}/api/v2/tables/{table_id}/records/{record_id}"
        response = requests.patch(url, headers=self.headers, json=data)
        return response
    
    def delete_record(self, table_id: str, record_id: str) -> requests.Response:
        """Удалить запись"""
        url = f"{self.base_url}/api/v2/tables/{table_id}/records/{record_id}"
        response = requests.delete(url, headers=self.headers)
        return response