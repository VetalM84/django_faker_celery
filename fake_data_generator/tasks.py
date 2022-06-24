import csv
from typing import Any, List

from faker import Faker

from django_faker_celery.celery import app

fake = Faker()


def make_csv(data: List[Any]):
    headers: List[str] = ["name", "phone", "email"]
    with open(file="fake_data.csv", mode="w", encoding="UTF-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers)
        writer.writerows(data)
    return csv_file


@app.task
def send_email(email):
    return f"Email sent to {email}"


@app.task
def generate_fake_data(total: int):
    fake_data: List[Any] = []
    for _ in range(total):
        name = fake.name()
        phone = fake.phone_number()
        email = fake.email()
        fake_data.append([name, phone, email])

    csv_file = make_csv(data=fake_data)

    send_email.delay("test@test.vv")

    return f"{total} random data rows created"
