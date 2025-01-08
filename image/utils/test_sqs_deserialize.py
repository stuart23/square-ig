from json.decoder import JSONDecodeError
from types import GeneratorType
from pytest import raises

from .sqs_deserialize import SQSDeserialize


def test_sqs_deserialize():
    event = {
        "Records":[
            {
                "messageId":"37b50a58-22cb-41fb-ab61-7827181625b7",
                "receiptHandle":"AQEBpDDyMztCUehw020wNpD7UOPIdzegtGKaU68DQhBjdqBoRY/M013hVGR+0/4fT4fNQa+OlH9xZSHgg1EyJok9Thvc5v7SZ2I8uJ74W9urL21585f6u7zUPWR3Wx6v8j3i7GG9Pf6vw8TqbCIxgkTrPnETCwnRAtwpwdw8a1/htJIemDjlmi5lFTv3/Q0RqYKv0kt9jlIiz9SBl3DxWd5yl/A0ryLnqeKBqKeTC7eWG/BvNmQZde8Lc5A7GNXd/NpxPr/ESMr+iesCfSfkmLqbecYoQzfRPcJFxPZ3Xz58j4l7WPQiiYCEdRytS2Sva9m7HK5RP4um+EULZ41kLQ9q9ZX6Xmlofc/69XiTLTw0bSfDexA0njWwLUsM9DjV2b2D",
                "body":"{\"action\": \"new_connection\", \"data\": {\"code\": \"sq0cgp-o1PUXWuX5nY-tqAMuG7GHg\", \"state\": \"82201dd8d83d23cc8a48caf52b\", \"response_type\": \"code\"}}",
                "attributes":{
                    "ApproximateReceiveCount":"1",
                    "AWSTraceHeader":"Root=1-677decd5-571d1fa85d77c4ba482f1464;Parent=3b3c86691caeaf42;Sampled=0;Lineage=1:031920b4:0",
                    "SentTimestamp":"1736305881223",
                    "SenderId":"AROAQHBTKKYL4JVWVY7LG:dev_oauth_callback",
                    "ApproximateFirstReceiveTimestamp":"1736305881231"
                },
                "messageAttributes":{
                    
                },
                "md5OfBody":"795775fd8748be4da279dbec60ea27ce",
                "eventSource":"aws:sqs",
                "eventSourceARN":"arn:aws:sqs:us-east-1:015140017687:dev_auth",
                "awsRegion":"us-east-1"
            }
        ]
    }

    generator = SQSDeserialize(event)
    assert isinstance(generator, GeneratorType)
    record = next(generator)

    # Should only have one record, so calling next on the generator again will fail.
    with raises(StopIteration):
        next(generator)
    
    assert record == {
        "action": "new_connection",
        "data": {
            "code": "sq0cgp-o1PUXWuX5nY-tqAMuG7GHg",
            "state": "82201dd8d83d23cc8a48caf52b",
            "response_type": "code"
        }
    }


def test_sqs_not_str():
    event = {
        "Records":[
            {
                "messageId":"37b50a58-22cb-41fb-ab61-7827181625b7",
                "body":12,
            }
        ]
    }

    generator = SQSDeserialize(event)
    with raises(TypeError) as e:
        next(generator)


def test_sqs_not_valid_json():
    event = {
        "Records":[
            {
                "messageId":"37b50a58-22cb-41fb-ab61-7827181625b7",
                "body":"{\"action\": \"new_connection\", \"data\": {\"code\": \"sq0cgp-o1PUXWuX5nY-tqAMuG7",
            }
        ]
    }

    generator = SQSDeserialize(event)
    with raises(JSONDecodeError) as e:
        next(generator)
