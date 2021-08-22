import random
import logging
from fifteen_puzzle.utils.impossible_fifteen_puzzle import *
logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger()

def test_idx_to_xy1():
    arr1 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    idx = find_idx(arr1, 1)
    assert idx == 0
    x, y = idx_to_xy(idx)
    assert x == 0 and y == 0
    
    idx = find_idx(arr1, 8)
    assert idx == 7
    x, y = idx_to_xy(idx)
    assert x == 3 and y == 1
    
    idx = find_idx(arr1, 16)
    assert idx == 15
    x, y = idx_to_xy(idx)
    assert x == 3 and y == 3
    
    idx = find_idx(arr1, 15)
    assert idx == 14
    x, y = idx_to_xy(idx)
    assert x == 2 and y == 3

def test_rearrange1():
    arr1 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    arr2 = [15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,16]
    n_swap = rearrange(arr1, arr2)
    LOGGER.debug(f'Swap {n_swap} times')
    assert n_swap == 7

def test_rearrange2():
    for i in range(10):
        arr1 = [i for i in range(200)]
        arr2 = arr1.copy()
        random.shuffle(arr2)
        LOGGER.debug(arr1)
        LOGGER.debug(arr2)
        _ = rearrange(arr1, arr2)
        assert arr1 == arr2

def test_check_solvability1():
    # initial configuration        target configuration
    # [ 1  2  3  4]                [15 14 13 12]
    # [ 5  6  7  8]                [11 10  9  8]
    # [ 9 10 11 12]                [ 7  6  5  4]
    # [13 14 15  X]                [ 3  2  1  X]
    
    arr1 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    arr2 = [15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,16]
    assert check_solvability(arr1, arr2) == False

def test_check_solvability2():
    # initial configuration        target configuration
    # [ 1  2  3  4]                [ 1  2  3  4]
    # [ 5  6  7  8]                [12 13 14  5]
    # [ 9 10 11 12]                [11  X 15  6]
    # [13 14 15  X]                [10  9  8  7]
    
    arr1 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    arr2 = [1,2,3,4,12,13,14,5,11,16,15,6,10,9,8,7]
    assert check_solvability(arr1, arr2) == True