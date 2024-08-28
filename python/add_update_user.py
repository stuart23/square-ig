
def handler(event, context):
    try:
        square_event_type = event['type']
        data = event['data']
    except KeyError:
        raise KeyError('Could not parse event: ', event)
    if data['type'] != 'customer':
        raise TypeError('Received non customer data type.')
    id = data['id']
    print(f'Looking for user {id}')