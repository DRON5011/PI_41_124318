from locust import HttpUser, task, between
import random

class UsersOnlyUser(HttpUser):
    wait_time = between(0.5, 2)
    token = "h070wPAEcnvRUrqeXswZu-LP7HZqnqZCo5PQudOg"
    
    def on_start(self):
        self.headers = {"xc-token": self.token, "Content-Type": "application/json"}
        self.table_id = "mxwx2ut83p8ft5c"
    
    @task(10)
    def get_students(self):
        self.client.get(
            f"/api/v2/tables/{self.table_id}/records",
            headers=self.headers,
            params={"limit": 50, "offset": 0}
        )
    
    @task(5)
    def get_student_by_id(self):
        self.client.get(
            f"/api/v2/tables/{self.table_id}/records",
            headers=self.headers,
            params={"where": "(Id,eq,3)", "limit": 1}
        )
    
    @task(3)
    def search_by_email(self):
        self.client.get(
            f"/api/v2/tables/{self.table_id}/records",
            headers=self.headers,
            params={"where": "(email,like,%Test%)", "limit": 10}
        )