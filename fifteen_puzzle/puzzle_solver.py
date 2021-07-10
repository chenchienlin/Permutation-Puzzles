from collections import deque
from os import stat
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
        # predecessor = prev[list_to_str(state)]
        successors = compute_successors(state, initial=initial)
        for suc in successors:
            # LOGGER.debug(f'Successors state {suc}  Valid {suc!=predecessor}')
            if list_to_str(suc) not in prev:
                prev[list_to_str(suc)] = state
                Q.append(suc)
            else:
                LOGGER.debug('Duplicate')
    
    return construct_moves(state, prev)


def DFSSolver(initial, goal, max_depth):
    BLANK = 16
    S = deque()
    S.append(initial)
    
    initial_str= list_to_str(initial)
    prev = dict()
    prev[initial_str] = None
    
    visited = dict()
    visited[initial_str] = False
    
    depth = dict()
    depth[initial_str] = 0
    state = None
    while len(S) > 0:
        state = S.pop()
        state_str = list_to_str(state)
        if visited[state_str] is False:
            visited[state_str] = True
            if state == goal:
                LOGGER.debug('Found goal')
                break
            if depth[state_str] > max_depth:
                # LOGGER.debug('Maximum depth')
                continue
            else:
                successors = compute_successors(state, initial=initial)
                for suc in successors:
                    suc_str = list_to_str(suc)
                    # if suc_str not in visited or visited[suc_str] is False:
                    if suc_str not in visited:
                        visited[suc_str] = False
                        prev[suc_str] = state
                        depth[suc_str] = depth[state_str] + 1
                        # LOGGER.debug(f'depth {depth[suc_str]}')
                        S.append(suc)
                    # else:
                    #     LOGGER.debug('Duplicate')
    if state != goal:
        LOGGER.warning('Not found goal')
        return DFSSolver(initial, goal, int(max_depth * 1.1))
    else:
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