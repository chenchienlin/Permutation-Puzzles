import heapq
from collections import deque
from fifteen_puzzle.puzzle_solver_util import *
from fifteen_puzzle.impossible_fifteen_puzzle import check_solvability
import logging
logging.basicConfig(level=logging.INFO)
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

def UCSSolver(initial, goal):
    BLANK = 16
    PQ = list()
    path_cost = 0
    heapq.heappush(PQ, (path_cost, initial))
    cost = dict()
    cost[list_to_str(initial)] = path_cost
    prev = dict()
    prev[list_to_str(initial)] = None
    explored = set()
    state = None
    
    while len(PQ) > 0:
        while True:
            tup = heapq.heappop(PQ)
            path_cost, state = tup[0], tup[1]
            state_str = list_to_str(state)
            if state_str not in explored:
                break
        LOGGER.debug(f'Proccessed state {state}')
        if state == goal:
            break
        
        explored.add(state_str)
        successors = compute_successors(state, initial=initial)
        for suc in successors:
            suc_str = list_to_str(suc)
            suc_path_cost = path_cost + 1
            if suc_str not in prev: # if the suc state haven't been found yet
                prev[suc_str] = state
                cost[suc_str] = suc_path_cost
                heapq.heappush(PQ, (suc_path_cost, suc))
            elif suc_str in prev and suc_str not in explored:
                old_path_cost = cost[suc_str]
                if suc_path_cost < old_path_cost:
                    prev[suc_str] = state
                    cost[suc_str] = suc_path_cost
                    heapq.heappush(PQ, (suc_path_cost, suc))
    
    return construct_moves(goal, prev)


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


def AStarSolver(initial, goal):
    BLANK = 16
    initial_str= list_to_str(initial)
    g_cost = dict()
    h_cost = dict()
    path_cost = 0
    g_cost[initial_str] = path_cost
    
    heuristic = manhattan_distance(initial, goal)
    # heuristic = misplace(initial, goal)
    
    PQ = list()
    f_cost = g_cost[initial_str] + heuristic
    heapq.heappush(PQ, (f_cost, initial))
    
    prev = dict()
    prev[initial_str] = None
    explored = set()
    state = None
    while len(PQ) > 0:
        while True:
            tup = heapq.heappop(PQ)
            f_cost, state = tup[0], tup[1]
            state_str = list_to_str(state)
            path_cost = g_cost[state_str]
            if state_str not in explored:
                break
        LOGGER.debug(f'Proccessed state {state}')
        if state == goal:
            break
        
        explored.add(state_str)
        successors = compute_successors(state, initial=initial)
        for suc in successors:
            suc_str = list_to_str(suc)
            
            heuristic = manhattan_distance(suc, goal)
            # heuristic = misplace(suc, goal)
            
            suc_f_cost = path_cost + 1 + heuristic
            if suc_str not in prev: # if the suc state haven't been found yet
                prev[suc_str] = state
                g_cost[suc_str] = path_cost + 1
                heapq.heappush(PQ, (suc_f_cost, suc))
            elif suc_str in prev and suc_str not in explored:
                old_g_cost = g_cost[suc_str]
                if path_cost + 1 < old_g_cost:
                    prev[suc_str] = state
                    g_cost[suc_str] = path_cost + 1
                    heapq.heappush(PQ, (suc_f_cost, suc))
    return construct_moves(goal, prev)

def RBFSSolver(initial, goal):
    prev, _ = RBFS(initial, initial, goal, 0, float('inf'))
    prev[list_to_str(initial)] = None
    return construct_moves(goal, prev)

def RBFS(initial, state, goal, curr_depth, f_limit):
    if state == goal:
        return {}, f_limit
    successors = compute_successors(state, initial=initial)
    PQ = list()
    for suc in successors:
        heuristic = manhattan_distance(suc, goal)
        suc_f_cost = curr_depth + heuristic
        PQ.append((suc_f_cost, suc))
    heapq.heapify(PQ)
    
    while True:
        tup = heapq.heappop(PQ)
        best_f, best_suc = tup[0], tup[1]
        if best_f > f_limit:
            return None, best_f
        
        if len(PQ) > 0:
            tup = PQ[0] # peek
            alter_f, alter_suc = tup[0], tup[1]
        else:
            alter_f = best_f
        prev, f_cost = RBFS(initial, best_suc, goal, curr_depth+1, min(f_limit, alter_f))
        heapq.heappush(PQ, (f_cost, best_suc))
        if prev is not None:
            LOGGER.debug(best_suc)
            prev[list_to_str(best_suc)] = state
            return prev, min(f_limit, alter_f)


if __name__ == '__main__':
    max_degree = 22
    initial = generate_puzzle(max_degree)
    size = 16
    goal = [i+1 for i in range(size)]
    solvable = check_solvability(initial, goal)
    LOGGER.debug(f'Puzzle : {initial}')
    LOGGER.debug(f'Solvable : {solvable}')
    _, moves_astar = AStarSolver(initial, goal)
    _, moves_rbfs = RBFSSolver(initial, goal)
    LOGGER.debug(len(moves_rbfs))
    assert len(moves_astar) == len(moves_rbfs)
    #_, moves_dls = DLSSolver(initial, goal, max_degree)
    # _, moves_bfs = BFSSolver(initial, goal)
    # _, moves_ids = IDSSolver(initial, goal, max_degree)
    # assert len(moves) == len(moves_ids)
    # from fifteen_puzzle.puzzle_solver_pygame import main
    # main(initial, moves=moves_astar, trace=True)