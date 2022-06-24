import csv
from datetime import datetime
from typing import Any, List, TextIO

from faker import Faker

from django_faker_celery.celery import app

fake = Faker()


@app.task
def make_csv(data: List[Any]) -> TextIO:
    current_time = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    headers: List[str] = ["name", "phone", "email"]
    with open(file=f"data_files/fake_data_{current_time}.csv", mode="w", encoding="UTF-8", newline="") as csv_file:
        writer = csv.writer(
            csv_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        writer.writerow(headers)
        writer.writerows(data)
    return csv_file


@app.task
def generate_fake_data(total: int):
    fake_data: List[Any] = []
    for _ in range(total):
        name = fake.name()
        phone = fake.phone_number()
        email = fake.email()
        fake_data.append([name, phone, email])

    csv_file = make_csv(data=fake_data)

    return f"{total} random data rows created, file: {csv_file.name}"
