
def handler(event, context):
    square_event_type = event['type']
    data = event['data']
    if data['type'] != 'customer':
        raise TypeError('Received non customer data type.')
    id = data['id']
    print(f'Looking for user {id}')