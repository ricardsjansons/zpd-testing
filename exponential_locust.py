import time

from gevent import sleep, spawn
from locust import HttpUser, between, task
from locust.env import Environment
from locust.stats import StatsCSVFileWriter, stats_printer


class MyUser(HttpUser):
    host = "http://192.168.101.8"
    wait_time = between(0, 0.01)

    @task
    def plaintext(self):
        self.client.get("/plaintext/")

    # @task
    # def json(self):
    #     self.client.get("/json/")

    # @task
    # def template(self):
    #     self.client.get("/template/locust-test/")

    # @task(3)  # weighted: insert more often
    # def insert(self):
    #     self.client.get("/db/insert/locust-test/")

    # @task(2)
    # def select(self):
    #     self.client.get("/db/select/locust-test/")

    # @task(1)
    # def delete(self):
    #     self.client.get("/db/delete/locust-test/")


# create Environment and Runner
env = Environment(user_classes=[MyUser])
runner = env.create_local_runner()

# CSV writer
percentiles = [50, 66, 75, 80, 90, 95, 98, 99, 99.9, 99.99]
csv_writer = StatsCSVFileWriter(
    environment=env, percentiles_to_report=percentiles, base_filepath="db", full_history=True)
spawn(csv_writer)

# --- Periodic stats output ---
spawn(stats_printer, env.runner.stats)

# --- Exponential ramp-up ---


def ramp_up():
    max_users = 1000
    step_seconds = 10
    growth_factor = 1.5

    users = 1
    start_time = time.time()

    while users <= max_users:
        env.runner.start(user_count=users, spawn_rate=users)
        print(f"[RAMP] Users={users}")
        sleep(step_seconds)
        users = int(users * growth_factor)


spawn(ramp_up)

# Keep process alive
while True:
    sleep(1)
