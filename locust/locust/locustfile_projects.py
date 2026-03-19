from locust import HttpUser, task, between
import random

class LectionsDoned(HttpUser):
    wait_time = between(1, 3)
    token = "h070wPAEcnvRUrqeXswZu-LP7HZqnqZCo5PQudOg"
    
    def on_start(self):
        self.headers = {"xc-token": self.token, "Content-Type": "application/json"}
        self.table_id = "m4i2yylgaqvy4m5"
    
    @task(8)
    def get_lections(self):
        self.client.get(
            f"/api/v2/tables/{self.table_id}/records",
            headers=self.headers,
            params={"limit": 20, "offset": 0}
        )
    
    @task(2)
    def get_lections(self):
        self.client.get(
            f"/api/v2/tables/{self.table_id}/records",
            headers=self.headers,
            params={"where": "(status,eq,%Проведена%)", "limit": 20}
        )