import heapq
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
        LOGGER.debug(f'Proccessed state {state}')
        if state == goal:
            break
        successors = compute_successors(state, initial=initial)
        for suc in successors:
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
                LOGGER.debug('Maximum depth')
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
                        S.append(suc)
    if state != goal:
        LOGGER.warning('Not found goal')
        return DFSSolver(initial, goal, int(max_depth * 1.1))
    else:
        return construct_moves(state, prev)


def DLSSolver(initial, goal, max_depth):
    prev = recur_DLS(initial, initial, goal, max_depth)
    if prev is not None:
        return construct_moves(goal, prev)
    else:
        return None, None


def recur_DLS(initial, state, goal, max_depth):
    if state == goal:
        return {list_to_str(initial):None}
    elif max_depth == 0:
        LOGGER.debug(f'Reached maximum depth')
        return None
    else:
        successors = compute_successors(state, initial=initial)
        for suc in successors:
            prev = recur_DLS(initial, suc, goal, max_depth-1)
            if prev is not None:
                prev[list_to_str(suc)] = state
                LOGGER.debug(state)
                return prev
        return None


def IDSSolver(initial, goal, max_depth):
    depth = 0
    moves = None
    while moves is None and depth <= max_depth:
        curr, moves = DLSSolver(initial, goal, depth)
        depth += 1
    return curr, moves


def BestFSSolver(initial, goal):
    BLANK = 16
    PQ = list()
    cost = manhattan_distance(initial, goal)
    heapq.heappush(PQ, (cost, initial))
    prev = dict()
    prev[list_to_str(initial)] = None
    state = None
    while len(PQ) > 0:
        tup = heapq.heappop(PQ)
        cost, state = tup[0], tup[1]
        LOGGER.debug(f'Proccessed state {state}')
        if state == goal:
            break
        successors = compute_successors(state, initial=initial)
        for suc in successors:
            if list_to_str(suc) not in prev:
                prev[list_to_str(suc)] = state
                cost = manhattan_distance(suc, goal)
                heapq.heappush(PQ, (cost, suc))
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
    # _, moves = BFSSolver(initial, goal)
    # _, moves_ids = IDSSolver(initial, goal, max_degree)
    # assert len(moves) == len(moves_ids)
    # from fifteen_puzzle.puzzle_solver_pygame import main
    # main(initial, moves, trace=True)