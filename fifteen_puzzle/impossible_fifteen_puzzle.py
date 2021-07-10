def find_idx(arr, target):
    for i in range(0, len(arr)):
        if arr[i] == target:
            return i

import math
def idx_to_xy(idx, n_col=4):
    # index               coordinate
    # [ 0  1  2  3]       [(0,0) (0,1) (0,2) (0,3)]
    # [ 4  5  6  7]       [(1,0) (1,1) (1,2) (1,3)]
    # [ 8  9 10 11]       [(2,0) (2,1) (2,2) (2,3)]
    # [12 13 14 15]       [(3,0) (3,1) (3,2) (3,3)]
    
    y = math.floor(idx/n_col)
    x = idx - y * n_col
    return x, y

def swap(arr, i, j):
    temp = arr[i]
    arr[i] = arr[j]
    arr[j] = temp

def rearrange(arr1, arr2):
    n_swap = 0
    for i in range(0, len(arr1)):
        if arr1[i] == arr2[i]:
            continue
        
        target = arr2[i]
        tar_idx = find_idx(arr1, target)
        swap(arr1, i, tar_idx)
        n_swap += 1
    return n_swap

def check_solvability(arr1, arr2):
    arr1 = arr1.copy()
    arr2 = arr2.copy()
    idx_16_init = find_idx(arr1, 16)
    idx_16_final = find_idx(arr2, 16)
    x1, y1 = idx_to_xy(idx_16_init)
    x2, y2 = idx_to_xy(idx_16_final)
    dist_16 = abs(x1-x2) + abs(y1-y2)
    n_swap = rearrange(arr1, arr2)
    mod1 = dist_16 % 2
    mod2 = n_swap % 2
    if mod1 != mod2:
        return False
    else:
        return True