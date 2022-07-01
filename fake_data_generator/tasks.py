"""Tasks for Celery"""
import csv
import logging
import os
from typing import Any, List
from io import StringIO

import boto3
from botocore.exceptions import ClientError
from faker import Faker

from django_faker_celery.celery import app
from django_faker_celery.storage_backends import StaticStorage, PublicMediaStorage

fake = Faker()


@app.task
def upload_file(file_name, bucket, data):
    """Upload a file to an S3 bucket."""
    # If S3 object_name was not specified, use file_name
    # if object_name is None:
    #     object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client("s3")
    # raw_file = bytes(file_name.getvalue())  # convert to bytes
    try:
        response = s3_client.put_object(
            Body=data.getvalue(), Bucket=bucket, Key=f"upload/{file_name}.csv"
        )
        # response = s3_client.put_object(raw_file, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


@app.task
def make_csv(data: List[Any]) -> StringIO:
    """Produce csv file with generated fake data and name it as task id."""
    headers: List[str] = ["name", "phone", "email"]

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

    csv_file = make_csv(data=fake_data)
    upload_file(
        file_name=self.request.id,
        bucket=os.getenv("AWS_STORAGE_BUCKET_NAME"),
        data=csv_file,
    )
    return f"{total} random data rows created."
