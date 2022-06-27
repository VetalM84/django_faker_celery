import csv
import os
from typing import Any, List

from faker import Faker

from django_faker_celery.celery import app

fake = Faker()


@app.task
def make_csv(data: List[Any], task_id: str):
    headers: List[str] = ["name", "phone", "email"]
    try:
        os.mkdir(path="tmp")
    except FileExistsError:
        print("Directory already exists")

    file_path = os.path.normpath(f"tmp/{task_id}.csv")
    with open(file=file_path, mode="w", encoding="UTF-8", newline="") as csv_file:
        writer = csv.writer(
            csv_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        writer.writerow(headers)
        writer.writerows(data)
    return True


@app.task(bind=True)
def generate_fake_data(self, total: int):
    fake_data: List[Any] = []
    for _ in range(total):
        name = fake.name()
        phone = fake.phone_number()
        email = fake.email()
        fake_data.append([name, phone, email])

    make_csv(data=fake_data, task_id=self.request.id)

    return f"{total} random data rows created."
