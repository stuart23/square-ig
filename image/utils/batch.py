def batch(batch_size):
    '''
    A decorator which will call the function in batches up to the size
    defined in the batch size.
    '''
    def wrap(function):
        def wrapped_f(*args, **kwargs):
            if 'items' in kwargs.keys():
                items = kwargs['items']
            elif len(args) == 2:
                items = args[1]
            else:
                raise ValueError(f'Items not passed. Args are {args}. Kwargs are {kwargs}')
            start_index = 0
            while True:
                end_index = min(start_index + batch_size, len(items))
                function(*args, items[start_index:end_index])
                if end_index == len(items):
                    break
                start_index += batch_size
        return wrapped_f
    return wrap