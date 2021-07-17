import logging
from fifteen_puzzle.puzzle_solver_util import *
logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger()

def test_find_idx():
    size = 16
    puzzle = [i+1 for i in range(size)]
    blank = 16
    idx = find_idx(puzzle, blank)
    assert idx == 15

def test_find_ngbrs():
    # index               coordinate
    # [ 0  1  2  3]       [(0,0) (0,1) (0,2) (0,3)]
    # [ 4  5  6  7]       [(1,0) (1,1) (1,2) (1,3)]
    # [ 8  9 10 11]       [(2,0) (2,1) (2,2) (2,3)]
    # [12 13 14 15]       [(3,0) (3,1) (3,2) (3,3)] 
    
    idx = 0
    ngbrs =  find_ngbrs(idx)
    LOGGER.debug(f'{idx} ngbrs : {ngbrs}')
    assert ngbrs == [None, None, 1, 4]
    
    idx = 5
    ngbrs =  find_ngbrs(idx)
    LOGGER.debug(f'{idx} ngbrs : {ngbrs}')
    assert ngbrs == [4, 1, 6, 9]
    
    idx = 10
    ngbrs =  find_ngbrs(idx)
    LOGGER.debug(f'{idx} ngbrs : {ngbrs}')
    assert ngbrs == [9, 6, 11, 14]
    
    idx = 3
    ngbrs =  find_ngbrs(idx)
    LOGGER.debug(f'{idx} ngbrs : {ngbrs}')
    assert ngbrs == [2, None, None, 7]
    
    idx = 12
    ngbrs =  find_ngbrs(idx)
    LOGGER.debug(f'{idx} ngbrs : {ngbrs}')
    assert ngbrs == [None, 8, 13, None]
    
    idx = 15
    ngbrs =  find_ngbrs(idx)
    LOGGER.debug(f'{idx} ngbrs : {ngbrs}')
    assert ngbrs == [14, 11, None, None]

def test_swap1():
    size = 16
    puzzle = [i+1 for i in range(size)]
    print_puzzle(puzzle)
    idx = 10
    ngbrs =  find_ngbrs(idx)
    top = ngbrs[1]
    swap(puzzle, idx, top)
    LOGGER.debug(f'Swap {puzzle[idx]} and {puzzle[top]}')
    print_puzzle(puzzle)
    assert puzzle == [1,2,3,4,5,6,11,8,9,10,7,12,13,14,15,16]

def test_swap2():
    size = 16
    puzzle = [i+1 for i in range(size)]
    print_puzzle(puzzle)
    blank = 16
    idx = find_idx(puzzle, blank)
    ngbrs =  find_ngbrs(idx)
    top = ngbrs[1]
    swap(puzzle, idx, top)
    print_puzzle(puzzle)
    
    idx = find_idx(puzzle, blank)
    assert idx == top
    ngbrs =  find_ngbrs(idx)
    left = ngbrs[0]
    swap(puzzle, idx, left)
    print_puzzle(puzzle)
    assert puzzle == [1,2,3,4,5,6,7,8,9,10,16,11,13,14,15,12]

def test_compute_successors1():
    size = 16
    puzzle = [i+1 for i in range(size)]
    print_puzzle(puzzle)
    successors = compute_successors(puzzle)
    for suc in successors:
        print_puzzle(suc)
    
    left_suc = successors[0]
    top_suc = successors[1]
    assert left_suc == [1,2,3,4,5,6,7,8,9,10,11,12,13,14,16,15]
    assert top_suc == [1,2,3,4,5,6,7,8,9,10,11,16,13,14,15,12]

def test_compute_successors2():
    # index               coordinate
    # [ 0  1  2  3]       [ 1  2  3  4]
    # [ 4  5  6  7]       [ 5  6  7  8]
    # [ 8  9 10 11]       [ 9 10 11 12]
    # [12 13 14 15]       [13 14 15 16]
    
    size = 16
    puzzle = [i+1 for i in range(size)]
    print_puzzle(puzzle)
    successors = compute_successors(puzzle, blank_idx=5)
    left_suc = successors[0]
    top_suc = successors[1]
    right_suc = successors[2]
    down_suc = successors[3]
    
    assert left_suc == [1,2,3,4,6,5,7,8,9,10,11,12,13,14,15,16]
    assert top_suc == [1,6,3,4,5,2,7,8,9,10,11,12,13,14,15,16]
    assert right_suc == [1,2,3,4,5,7,6,8,9,10,11,12,13,14,15,16]
    assert down_suc == [1,2,3,4,5,10,7,8,9,6,11,12,13,14,15,16]

def test_manhattan_distance1():
    size = 16
    goal = [i+1 for i in range(size)]
    initial = goal.copy()
    swap(initial, 0, 15)
    
    print_puzzle(initial, name='Initial')
    print_puzzle(goal, name='Goal')
    assert manhattan_distance(initial, goal) == 12
    
    initial = goal.copy()
    swap(initial, 11, 15)
    print_puzzle(initial, name='Initial')
    print_puzzle(goal, name='Goal')
    assert manhattan_distance(initial, goal, n_col=4) == 2

def test_manhattan_distance2():
    # initial           goal
    # [ 7  2  4 ]       [ 9  1  2 ]
    # [ 5  9  6 ]       [ 3  4  5 ]
    # [ 8  3  1 ]       [ 6  7  8 ]
    size = 9
    goal = [i+1 for i in range(size-1)]
    goal.insert(0, size)
    initial = [7,2,4,5,9,6,8,3,1]
    print_puzzle(initial, n_col=3, n_row=3, name='Initial')
    print_puzzle(goal, n_col=3, n_row=3, name='Goal')
    assert manhattan_distance(initial, goal, n_col=3) == 18