from collections import deque
from fifteen_puzzle.puzzle_solver_util import *
from fifteen_puzzle.impossible_fifteen_puzzle import check_solvability
import logging
logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger()

def BFSSolver(initial, goal):
    BLANK = 16
    Q = deque()
    Q.append(initial)
    prev = dict()
    prev[list_to_str(initial)] = None
    state = None
    while True:
        state = Q.popleft()
        # LOGGER.debug(f'Proccessed state {state}')
        if state == goal:
            # return prev
            break
        predecessor = prev[list_to_str(state)]
        successors = compute_successors(state, initial=initial)
        for suc in successors:
            LOGGER.debug(f'Successors state {suc}  Valid {suc!=predecessor}')
            if suc != predecessor:
                prev[list_to_str(suc)] = state
                Q.append(suc)
            else:
                LOGGER.debug('Duplicate')
    
    return construct_moves(state, prev)

if __name__ == '__main__':
    max_degree = 11
    initial = generate_puzzle(max_degree)
    size = 16
    goal = [i+1 for i in range(size)]
    solvable = check_solvability(initial, goal)
    LOGGER.debug(f'Puzzle : {initial}')
    LOGGER.debug(f'Solvable : {solvable}')
    _, moves = BFSSolver(initial, goal)
    
    from fifteen_puzzle.puzzle_solver_pygame import main
    main(initial, moves, trace=True)