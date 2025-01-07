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
    elif code := queryStringParameters.get('code'):
        publish({
            'code': code,
            'state': queryStringParameters.get('state'),
            'response_type': queryStringParameters.get('response_type'),
        })
    else:
        raise Exception('Not sure')
