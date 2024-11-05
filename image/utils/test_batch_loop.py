from .batch_loop import batch_loop


def test_batch_loop_1():
    x = list(range(20))
    output = []
    batch_loop(x, 5, output.append)
    assert output[0] == [0,1,2,3,4]
    assert output[1] == [5,6,7,8,9]
    assert output[2] == [10,11,12,13,14]
    assert output[3] == [15,16,17,18,19]
    assert len(output) == 4


def test_batch_loop_2():
    x = list(range(11))
    output = []
    batch_loop(x, 5, output.append)
    assert output[0] == [0,1,2,3,4]
    assert output[1] == [5,6,7,8,9]
    assert output[2] == [10]
    assert len(output) == 3


def test_batch_loop_3():
    x = list(range(5))
    output = []
    batch_loop(x, 7, output.append)
    assert output[0] == [0,1,2,3,4]
    assert len(output) == 1