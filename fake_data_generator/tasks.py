import csv
import os
from typing import Any, List, TextIO

from faker import Faker

from django_faker_celery.celery import app

fake = Faker()


@app.task
def make_csv(data: List[Any], task_id: str) -> TextIO:
    headers: List[str] = ["name", "phone", "email"]
    try:
        os.mkdir(path="data_files")
    except FileExistsError:
        print("Directory already exists")

    file_path = os.path.normpath(f"data_files/{task_id}.csv")
    try:
        with open(file=file_path, mode="w", encoding="UTF-8", newline="") as csv_file:
            writer = csv.writer(
                csv_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            writer.writerow(headers)
            writer.writerows(data)
    except Exception as e:
        print(e)
    return csv_file


@app.task(bind=True)
def generate_fake_data(self, total: int):
    fake_data: List[Any] = []
    for _ in range(total):
        name = fake.name()
        phone = fake.phone_number()
        email = fake.email()
        fake_data.append([name, phone, email])

    csv_file = make_csv(data=fake_data, task_id=self.request.id)

    return f"{total} random data rows created."
