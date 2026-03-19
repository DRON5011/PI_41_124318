from locust import FastHttpUser, task, between
import random

class MixedLoadUser(FastHttpUser):
    wait_time = between(0.1, 1)
    token = "h070wPAEcnvRUrqeXswZu-LP7HZqnqZCo5PQudOg"
    
    def on_start(self):
        self.headers = {"xc-token": self.token}
        self.tables = [
            ('Lections', 'm4i2yylgaqvy4m5'),
            ('Records', 'mxiqj9yx82ds334'),
            ('Teachers', 'm0s0n53zz8856sk'),
            ('Students', 'mxwx2ut83p8ft5c'),
            ('Problem_marks', 'mfjndhoxhp3hols'),
            ('Metaphors', 'mtzlwx9b3m6cz9b'),
        ]
    
    @task
    def random_get(self):
        name, table_id = random.choice(self.tables)
        self.client.get(
            f"/api/v2/tables/{table_id}/records",
            headers=self.headers,
            params={"limit": random.randint(10, 50)},
            name=f"GET /{name}"
        )