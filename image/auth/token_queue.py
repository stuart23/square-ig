from boto3 import client as Boto3Client
from json import dumps
from os import getenv
from utils import getenv_or_raise


def publish(message):
    QUEUE_URL = getenv_or_raise('QUEUE_URL')
    sqs_client = Boto3Client('sqs')
    print(f"Publishing the following to topic {QUEUE_URL}: {message}")
    response = sqs_client.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=message
    )
