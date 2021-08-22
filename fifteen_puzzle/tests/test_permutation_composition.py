import random
import logging
from fifteen_puzzle.utils.permutation_composition import *
logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger()

def test_permutation_composition1():
    a = [5,3,1,4,2]
    b = [5,3,2,1,4]
    assert permutation_composition(a, b) == [4,2,5,1,3]
    assert permutation_composition(b, a) == [2,1,3,5,4]

def test_permutation_composition2():
    a = [3,2,7,8,1,4,5,6]
    b = [5,2,1,6,7,8,3,4]
    assert permutation_composition(a, b) == [1,2,3,4,5,6,7,8]

def test_permutation_composition3():
    a = [3,4,1,5,2]
    a2 = permutation_composition(a, a)
    assert a2 == [1,5,3,2,4]
    
    a3 = permutation_composition(a, a2)
    assert a3 == [3,2,1,4,5]
    
    a4 = permutation_composition(a, a3)
    assert a4 == [1,4,3,5,2]
    
    a5 = permutation_composition(a, a4)
    assert a5 == [3,5,1,2,4]
    
    a6 = permutation_composition(a, a5)
    assert a6 == [1,2,3,4,5]

def test_inverse_permutation1():
    epsilon = [1,2,3,4,5,6,7,8]
    a = [3,2,7,8,1,4,5,6]
    b = inverse_permutation(a, epsilon)
    assert b == [5,2,1,6,7,8,3,4]
    assert permutation_composition(a, b) == epsilon

def test_associativity():
    epsilon = [1,2,3,4,5,6,7,8]
    a = [3,2,7,8,1,4,5,6]
    b = [5,2,1,6,7,8,3,4]
    a_inv = inverse_permutation(a, epsilon)
    b_inv = inverse_permutation(b, epsilon)
    ab = permutation_composition(a, b)
    inv_b_inv_a = permutation_composition(b_inv, a_inv)
    result = permutation_composition(ab, inv_b_inv_a)
    LOGGER.debug(result)
    assert result == epsilon