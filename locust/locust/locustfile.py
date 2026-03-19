from locust import HttpUser, task, between
import random
import json

class NocoDBUser(HttpUser):
    wait_time = between(1, 3)
    token = "h070wPAEcnvRUrqeXswZu-LP7HZqnqZCo5PQudOg"
    
    def on_start(self):
        self.headers = {
            "xc-token": self.token,
            "Content-Type": "application/json"
        }
        self.table_ids = {
            'Lections': 'm4i2yylgaqvy4m5',
            'Records': 'mxiqj9yx82ds334',
            'Teachers': 'm0s0n53zz8856sk',
            'Students': 'mxwx2ut83p8ft5c',
            'Problem_marks': 'mfjndhoxhp3hols',
            'Metaphors': 'mtzlwx9b3m6cz9b',
        }
    
    @task(7)
    def get_students(self):
        self.client.get(
            f"/api/v2/tables/{self.table_ids['Students']}/records",
            headers=self.headers,
            params={"limit": 20, "offset": 0},
            name="GET /Students"
        )
    
    @task(6)
    def get_records(self):
        self.client.get(
            f"/api/v2/tables/{self.table_ids['Records']}/records",
            headers=self.headers,
            params={"limit": 20, "offset": 0},
            name="GET /Records"
        )
    
    @task(5)
    def get_teachers(self):
        self.client.get(
            f"/api/v2/tables/{self.table_ids['Teachers']}/records",
            headers=self.headers,
            params={"limit": 20, "offset": 0},
            name="GET /Teachers"
        )
    
    @task(4)
    def get_lections(self):
        self.client.get(
            f"/api/v2/tables/{self.table_ids['Lections']}/records",
            headers=self.headers,
            params={"limit": 20, "offset": 0},
            name="GET /Lections"
        )
    
    @task(3)
    def get_problem_marks(self):
        self.client.get(
            f"/api/v2/tables/{self.table_ids['Problem_marks']}/records",
            headers=self.headers,
            params={"limit": 20, "offset": 0},
            name="GET /Problem_marks"
        )
    
    @task(2)
    def get_metaphors(self):
        self.client.get(
            f"/api/v2/tables/{self.table_ids['Metaphors']}/records",
            headers=self.headers,
            params={"limit": 20, "offset": 0},
            name="GET /Metaphors"
        )
    
    @task(1)
    def search_students(self):
        emails = ["Test1@test.ru", "Test2@test.ru", "Test3@test.ru"]
        self.client.get(
            f"/api/v2/tables/{self.table_ids['Students']}/records",
            headers=self.headers,
            params={"where": f"(email,like,%{random.choice(emails)}%)", "limit": 10},
            name="GET /Students/search"
        )