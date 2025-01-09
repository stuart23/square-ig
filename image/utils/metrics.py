from boto3 import client


class MetricsHandler():
    '''
    Convenience wrapper for emitting metrics to cloudwatch.
    '''
    def __init__(self, namespace):
        self.namespace = namespace
        self.client = client('cloudwatch')

    def emit_metric(self, metric_name, value, dimensions={}):
        '''
        Emits a metric to cloudwatch.
        '''
        self.client.put_metric_data(
            MetricData=[
                {
                    'MetricName': metric_name,
                    'Unit': 'None',
                    'Value': value,
                    'Dimensions': [
                        {
                            'Name': key,
                            'Value': value
                        } for key, value in dimensions.items()
                    ],
                },
            ],
            Namespace=self.namespace
        )
