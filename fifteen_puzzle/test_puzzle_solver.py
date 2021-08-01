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
        assert len(moves_bfs) <= max_degree

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

def test_IDSSolver1():
    iter = 100
    for _ in range(iter):
        max_degree = 10
        initial = generate_puzzle(max_degree)
        goal = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
        curr_bfs, moves_bfs = BFSSolver(initial, goal)
        curr_ids, moves_ids = IDSSolver(initial, goal, max_degree)
        assert curr_bfs == curr_ids == goal
        assert len(moves_bfs) == len(moves_ids)
        assert len(moves_ids) <= max_degree

def test_BestFSSolver1():
    iter = 100
    for _ in range(iter):
        max_degree = 11
        initial = generate_puzzle(max_degree)
        goal = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
        curr_best, _ = BestFSSolver(initial, goal)
        assert curr_best == goal

def test_UCSSolver_AStarSolver1():
    iter = 100
    for _ in range(iter):
        size = 16
        max_degree = 11
        initial = generate_puzzle(max_degree)
        goal = [i+1 for i in range(size)]
        sol1, moves_bfs = BFSSolver(initial, goal)
        sol2, moves_ucs = UCSSolver(initial, goal)
        sol3, moves_astar = AStarSolver(initial, goal)
        assert sol1 == sol2 == sol3 == goal
        assert len(moves_bfs) == len(moves_ucs)
        assert len(moves_bfs) == len(moves_astar)

def test_AStartSolver_RBFSSovler1():
    iter = 100
    for i in range(iter):
        size = 16
        max_degree = 15
        initial = generate_puzzle(max_degree)
        goal = [i+1 for i in range(size)]
        sol, moves_astar = AStarSolver(initial, goal)
        _, moves_rbfs = RBFSSolver(initial, goal)
        assert sol == goal
        assert len(moves_astar) <= max_degree
        assert len(moves_rbfs) <= max_degree
        assert len(moves_astar) == len(moves_rbfs)
        LOGGER.info(f'Iteration: {i}')

def test_RBFSSovler1():
    iter = 100
    for i in range(iter):
        size = 16
        max_degree = 20
        initial = generate_puzzle(max_degree)
        goal = [i+1 for i in range(size)]
        _, moves_rbfs = RBFSSolver(initial, goal)
        assert len(moves_rbfs) <= max_degree
        LOGGER.info(f'Iteration: {i}')