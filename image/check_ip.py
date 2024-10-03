permitted_ips = ('54.245.1.154', '34.202.99.168', '54.212.177.79', '107.20.218.8')

def handler(event, context):
    ip_address = event['requestContext']['http']['sourceIp']
    if ip_address in permitted_ips:
        print(f'Authorized IP {ip_address}')
        return True
    else:
        raise Exception('Unauthorized')