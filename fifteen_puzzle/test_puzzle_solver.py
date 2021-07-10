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
        sol, _ = BFSSolver(initial, goal)
        assert sol == goal