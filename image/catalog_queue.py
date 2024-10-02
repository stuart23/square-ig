from boto3 import client as Boto3Client
from json import dumps
from os import getenv

sns_client = Boto3Client('sns')
queue_arn = getenv('sns_arn')

def publish(message):
    response = sns_client.publish(
        TargetArn=queue_arn,
        Message=dumps({'default': dumps(message)}),
        MessageStructure='json'
    )
