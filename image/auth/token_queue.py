from json import dumps

from boto3 import client as Boto3Client
from utils import getenv_or_raise

QUEUE_URL_ENV_VAR = 'QUEUE_URL'


def publish(message):
    '''
    Sends the message to the auth queue to be processed.
    '''
    queue_url = getenv_or_raise(QUEUE_URL_ENV_VAR)
    sqs_client = Boto3Client("sqs")
    print(f"Publishing the following to topic {queue_url}: {message}")
    response = sqs_client.send_message(
        QueueUrl=queue_url,
        MessageBody=dumps(message)
    )
    return response
