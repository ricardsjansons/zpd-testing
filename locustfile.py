import os
import random
from string import ascii_lowercase

import dotenv
from locust import HttpUser, LoadTestShape, task

dotenv.load_dotenv()

EXP_BASE = float(os.environ["EXP_BASE"])
MIN_USERS = int(os.environ["MIN_USERS"])
MAX_USERS = int(os.environ["MAX_USERS"])
SPAWN_RATE = float(os.environ["SPAWN_RATE"])

RUN_TIME = float(os.environ["RUN_TIME"])


def rstr(k: int):
    return "".join(random.choices(ascii_lowercase, k=k))


def w(key: str):
    return int(os.environ[key])


class User(HttpUser):
    host = os.environ["HOST"]

    @task(w("PLAINTEXT"))
    def task_plaintext(self):
        self.client.get("/plaintext/")

    @task(w("JSON"))
    def task_json(self):
        self.client.get("/json/")

    @task(w("TEMPLATE"))
    def task_template(self):
        self.client.get(f"/template/{rstr(1000)}")

    @task(w("DB_SELECT"))
    def task_db_select(self):
        self.client.get(f"/db/select/{rstr(5)}/")

    @task(w("DB_INSERT"))
    def task_db_insert(self):
        self.client.get(f"/db/insert/{rstr(5)}/")

    @task(w("DB_DELETE"))
    def task_db_delete(self):
        self.client.get(f"/db/delete/{rstr(5)}/")


class Shape(LoadTestShape):
    def tick(self):
        t = self.get_run_time()
        users = EXP_BASE**t * MIN_USERS
        users = min(int(users), MAX_USERS)
        return (users, users) if t < RUN_TIME else None
