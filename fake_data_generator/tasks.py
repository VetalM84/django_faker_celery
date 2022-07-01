"""Tasks for Celery"""
import csv
import logging
import os
from io import StringIO
from typing import Any, List

import boto3
from botocore.exceptions import ClientError
from faker import Faker

from django_faker_celery.celery import app

fake = Faker()


@app.task
def upload_file(file_name: str, bucket: str, data: StringIO) -> bool:
    """Upload a file to an S3 bucket."""
    s3_client = boto3.client("s3")
    try:
        response = s3_client.put_object(
            Body=data.getvalue(), Bucket=bucket, Key=f"upload/{file_name}.csv"
        )
    except ClientError as e:
        logging.error(e)
        return False
    return True


@app.task
def make_csv(data: List[Any]) -> StringIO:
    """Generate a fake data and store it in memory."""
    headers: List[str] = ["name", "phone", "email"]

    # Create a StringIO object to store the data in memory
    file_buffer = StringIO()

    writer = csv.writer(
        file_buffer, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
    )
    writer.writerow(headers)
    writer.writerows(data)
    return file_buffer


@app.task(bind=True)
def generate_fake_data(self, total: int):
    """Generate fake data function."""
    fake_data: List[Any] = []
    for _ in range(total):
        name = fake.name()
        phone = fake.phone_number()
        email = fake.email()
        fake_data.append([name, phone, email])

    # Generate a CSV file to memory
    csv_in_memory = make_csv(data=fake_data)

    # Upload the CSV file to S3
    upload_file(
        file_name=self.request.id,
        bucket=os.getenv("AWS_STORAGE_BUCKET_NAME"),
        data=csv_in_memory,
    )
    return f"{total} random data rows created."
