from .batch import batch


def test_batch_1():
    output = []
    
    @batch(5)
    def func(items):
        output.append(items)
    x = list(range(20))
    func(items=x)
    assert output[0] == [0,1,2,3,4]
    assert output[1] == [5,6,7,8,9]
    assert output[2] == [10,11,12,13,14]
    assert output[3] == [15,16,17,18,19]
    assert len(output) == 4


def test_batch_loop_2():
    output = []
    
    @batch(5)
    def func(items):
        output.append(items)
    x = list(range(11))
    func(items=x)
    assert output[0] == [0,1,2,3,4]
    assert output[1] == [5,6,7,8,9]
    assert output[2] == [10]
    assert len(output) == 3


def test_batch_loop_3():
    output = []
    
    @batch(5)
    def func(items):
        output.append(items)
    x = list(range(5))
    func(items=x)
    assert output[0] == [0,1,2,3,4]
    assert len(output) == 1


def test_batch_loop_4():
    output = []
    
    @batch(5)
    def func(items):
        output.append(items)
    x = list(range(4))
    func(items=x)
    assert output[0] == [0,1,2,3]
    assert len(output) == 1