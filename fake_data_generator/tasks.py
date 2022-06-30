"""Tasks for Celery"""
import csv
import logging
import os
from typing import Any, List

import boto3
from botocore.exceptions import ClientError
from faker import Faker

from django_faker_celery.celery import app

fake = Faker()


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client("s3")
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


@app.task
def make_csv(data: List[Any], task_id: str):
    """Produce csv file with generated fake data and name it as task id."""
    headers: List[str] = ["name", "phone", "email"]

    file_path = os.path.normpath(os.path.basename(f"{task_id}.csv"))
    print(f"File path: {file_path}")
    with open(file=file_path, mode="w", encoding="UTF-8", newline="") as csv_file:
        writer = csv.writer(
            csv_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        writer.writerow(headers)
        writer.writerows(data)
        upload_file(
            file_name=csv_file,
            bucket=os.getenv("AWS_STORAGE_BUCKET_NAME"),
        )
    return True


@app.task(bind=True)
def generate_fake_data(self, total: int):
    """Generate fake data function."""
    fake_data: List[Any] = []
    for _ in range(total):
        name = fake.name()
        phone = fake.phone_number()
        email = fake.email()
        fake_data.append([name, phone, email])

    make_csv(data=fake_data, task_id=self.request.id)

    return f"{total} random data rows created."
