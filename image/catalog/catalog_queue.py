from boto3 import client as Boto3Client
from json import dumps
from os import getenv

sns_client = Boto3Client('sns')
TOPIC_ARN = getenv('sns_topic_arn')

def publish(message):
    print(f"Publishing the following to topic {TOPIC_ARN}: {message}")
    response = sns_client.publish(
        TopicArn=TOPIC_ARN,
        Message=dumps({'default': dumps(message)}),
        MessageStructure='json'
    )
