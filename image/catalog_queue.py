from boto3 import client as Boto3Client
from json import dumps
from os import getenv

sns_client = Boto3Client('sns')
topic_arn = getenv('sns_topic_arn')

def publish(message):
    print(f"Publishing the following to topic {topic_arn}: {message}")
    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=dumps({'default': dumps(message)}),
        MessageStructure='json'
    )
