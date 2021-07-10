def permutation_composition(a, b):
    assert len(a) == len(b)
    return [b[a[k] - 1] for k in range(len(a))]

def inverse_permutation(a, epsilon):
    assert len(a) == len(epsilon)
    inv = [None for _ in range(len(a))]
    for k in range(len(a)):
        val = epsilon[k]
        idx = a[k] - 1
        inv[idx] = val
    return inv