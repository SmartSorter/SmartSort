import random
from locust import HttpUser, task, between

class SmartSortLoadTest(HttpUser):
    wait_time = between(0.05, 0.2) 

    @task(2)
    def test_health_check(self):
        """Легкий запит перевірки працездатності сервера"""
        self.client.get("/api/health")

    @task(5)
    def test_device_lifecycle(self):
        """Важкий сценарій: реєстрація, авторизація диспетчера та перегляд баків"""
        fake_id = random.randint(1000, 999999)
        username = f"tester_{fake_id}"
        password = "testpassword123"
        
        self.client.post("/users", json={
            "username": username,
            "password": password,
            "role": "User"
        })
        

        login_response = self.client.post("/token", data={
            "username": username,
            "password": password
        })
        
       
        if login_response.status_code == 200:
            self.client.get("/api/devices")