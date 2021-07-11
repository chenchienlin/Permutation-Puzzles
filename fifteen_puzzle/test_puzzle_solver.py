import logging
from fifteen_puzzle.puzzle_solver import *
logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger()

def test_BFSSolver1():
    iter = 1000
    for _ in range(iter):
        max_degree = 5
        initial = generate_puzzle(max_degree)
        goal = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
        sol1, moves_bfs = BFSSolver(initial, goal)
        sol2, _ = DFSSolver(initial, goal, max_degree)
        assert sol1 == goal
        assert sol2 == goal

def test_DLSSolver1():
    max_depth = 1
    initial = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,16,15]
    goal = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    curr, moves = DLSSolver(initial, goal, max_depth)
    assert curr == goal
    assert len(moves) == max_depth

def test_DLSSolver2():
    max_depth = 1
    initial = [1,2,3,4,5,6,7,8,9,10,11,12,13,16,14,15]
    goal = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    _, moves = DLSSolver(initial, goal, max_depth)
    assert moves == None
    
    max_depth = 2
    curr, moves = DLSSolver(initial, goal, max_depth)
    assert curr == goal
    assert len(moves) == max_depth

def test_DLSSolver3():
    iter = 1000
    for _ in range(iter):
        max_degree = 5
        initial = generate_puzzle(max_degree)
        goal = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
        curr, moves = DLSSolver(initial, goal, max_degree)
        assert curr == goal
        assert len(moves) <= max_degree

def test_DLSSolver4():
    iter = 1000
    for _ in range(iter):
        max_degree = 5
        initial = generate_puzzle(max_degree)
        goal = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
        curr_dls, moves_dls = DLSSolver(initial, goal, max_degree)
        curr_bfs, moves_bfs = BFSSolver(initial, goal)
        assert curr_dls == curr_bfs == goal
        assert len(moves_dls) == len(moves_bfs)
        assert len(moves_dls) <= max_degree