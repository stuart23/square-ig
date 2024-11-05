def batch_loop(my_list, max_records, function):
    '''
    Applies the function to groups of my_list with a maximum
    of max_records per iteration.
    '''
    if len(my_list) > max_records:
        function(my_list[:max_records])
        batch_loop(my_list[max_records:], max_records, function)
    else:
        function(my_list)