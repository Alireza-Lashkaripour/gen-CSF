#!/usr/bin/env python3
import sympy
from sympy.physics.quantum.cg import CG

S_half = sympy.Rational(1, 2)
memo_paths = {}
memo_csf = {}
a = sympy.Function('a')
b = sympy.Function('b')

def find_paths_recursive(k, current_S, N_target, S_target):
    if (k, current_S) in memo_paths:
        return memo_paths[(k, current_S)]
    if k == N_target:
        return [[S_target]] if current_S == S_target else []
    if not (0 <= current_S <= k/2):
        return []
    paths = []
    for next_S in (current_S + S_half,):
        for p in find_paths_recursive(k+1, next_S, N_target, S_target):
            paths.append([current_S] + p)
    if current_S > 0:
        for p in find_paths_recursive(k+1, current_S - S_half, N_target, S_target):
            paths.append([current_S] + p)
    memo_paths[(k, current_S)] = paths
    return paths

def construct_csf(path, M):
    path_tuple = tuple(path)
    k = len(path_tuple) - 1
    S = path_tuple[-1]
    if (path_tuple, M) in memo_csf:
        return memo_csf[(path_tuple, M)]
    if abs(M) > S:
        return 0
    if k == 0:
        return 1 if S == 0 and M == 0 else 0
    S_parent = path_tuple[-2]
    c_alpha = CG(S_parent, M - S_half, S_half, S_half, S, M).doit()
    c_beta  = CG(S_parent, M + S_half, S_half, -S_half, S, M).doit()
    term_alpha = 0
    if c_alpha != 0:
        p = construct_csf(path_tuple[:-1], M - S_half)
        if p != 0:
            term_alpha = c_alpha * p * a(k)
    term_beta = 0
    if c_beta != 0:
        p = construct_csf(path_tuple[:-1], M + S_half)
        if p != 0:
            term_beta = c_beta * p * b(k)
    result = sympy.expand(term_alpha + term_beta)
    memo_csf[(path_tuple, M)] = result
    return result

def generate_csfs(N, S, M):
    S_sym = sympy.sympify(S)
    M_sym = sympy.sympify(M)
    # ensure half-integers become exact Rationals
    if isinstance(S_sym, sympy.Float):
        S_sym = sympy.Rational(int(2*S_sym), 2)
    if isinstance(M_sym, sympy.Float):
        M_sym = sympy.Rational(int(2*M_sym), 2)
    if S_sym < 0 or N < 0 or (N % 2 != (2*S_sym) % 2) or abs(M_sym) > S_sym:
        print("Invalid (N, S, M) combination.")
        return
    memo_paths.clear()
    memo_csf.clear()
    all_paths = find_paths_recursive(0, 0, N, S_sym)
    if not all_paths:
        print(f"No CSFs are possible for N={N}, S={S_sym}.")
        return
    print(f"Found {len(all_paths)} CSFs for N={N}, S={S_sym}, M={M_sym}\n")
    sympy.init_printing(use_unicode=True)
    for i, path in enumerate(all_paths):
        header = f"--- CSF #{i+1} (Path: {path}) ---"
        print(header)
        csf = construct_csf(path, M_sym)
        if csf == 0:
            print(" (This CSF is zero for the given M value)")
        else:
            p = sympy.simplify(sort_spin_functions(csf))
            sympy.pprint(p)
        print("-" * len(header), "\n")

if __name__ == '__main__':
    generate_csfs(4, 0, 0)

