from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        self.client.get("/")

    @task(3)
    def all_Courses(self):
        self.client.get("/courses")

    @task(1)
    def get_Course(self):
        self.client.get("/pare?coin=BTC&currency=GEL")
        self.client.get("/pare?coin=BTC&currency=KZT")
        self.client.get("/pare?coin=ETH&currency=RUB")
        self.client.get("/pare?coin=ETH&currency=USD")


