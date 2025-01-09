from json import loads
from json.decoder import JSONDecodeError


def SQSDeserialize(event):
    """
    Used to deserialize events from SQS. Provides some error checking.
    """
    for record in event["Records"]:
        messageId = record["messageId"]
        print(f"Processing messageId: {messageId}")

        body = record["body"]
        try:
            deserialized_body = loads(body)
        except TypeError as e:
            e.add_note(
                f"Message body was not a string. Message body received is {body}"
            )
            raise e
        except JSONDecodeError as e:
            e.add_note(f"Could not decode json. Message body received is {body}")
            raise e
        yield deserialized_body
