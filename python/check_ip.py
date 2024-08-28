
permitted_ips = ('54.245.1.154', '34.202.99.168', '54.212.177.79', '107.20.218.8')

def handler(event, context):
    if event['requestContext']['http']['sourceIp'] in permitted_ips:
        print('permitted')
    else:
        raise Exception('Unauthorized')