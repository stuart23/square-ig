# from auth.token_queue import publish

def handler(event, context):
    '''
    Adds the tenant to the dynamo table.
    '''
    print('EVENT')
    print(event)
    print('CONTEXT')
    print(context)
    # if code := event['queryStringParameters'].get('code'):
    #     publish({'code': code})
    # else:
    #     error = event['queryStringParameters'].get('error')
    #     error_description = event['queryStringParameters'].get('error_description')
    #     print(f'OAUTH ERROR: {error} - {error_description}')