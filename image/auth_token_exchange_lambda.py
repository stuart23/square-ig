from auth.token_queue import publish

def handler(event, context):
    print('EVENT')
    print(event)
    print('CONTEXT')
    print(context)