import csv
import os
from datetime import datetime
from typing import Any, List, TextIO

from faker import Faker

from django_faker_celery.celery import app

fake = Faker()


@app.task
def make_csv(data: List[Any]) -> TextIO:
    current_time = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    headers: List[str] = ["name", "phone", "email"]
    try:
        os.mkdir(path="data_files")
        file_path = os.path.normpath(f"data_files/{current_time}.csv")
        with open(file=file_path, mode="w", encoding="UTF-8", newline="") as csv_file:
            writer = csv.writer(
                csv_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            writer.writerow(row=headers)
            writer.writerows(rows=data)
    except FileNotFoundError:
        print("Error, can not create file. Contact support")
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
