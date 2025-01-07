from auth.token_queue import publish

def handler(event, context):
    '''
    We could not use a native SQS integration from the API Gateway
    because the querystrings in the callback change if it is an
    error or not.
    '''
    queryStringParameters = event['queryStringParameters']
    if error := queryStringParameters.get('error'):
        error_description = queryStringParameters.get('error_description')
        print(f'OAUTH ERROR: {error} - {error_description}')
        return {
            'statusCode': 500,
            'body': {'error': error, 'error_description': error_description}
        }
    elif code := queryStringParameters.get('code'):
        publish({
            'action': 'new_connection',
            'data': {
                'code': code,
                'state': queryStringParameters.get('state'),
                'response_type': queryStringParameters.get('response_type'),
            }
        })
        return {
            'statusCode' : 200,
            'body': "Event Handled"
        }

    else:
        print(f'Square response unknown. Event details: f{event}')
        return {
            'statusCode' : 400,
            'body': "Square did not return an expected response."
        }