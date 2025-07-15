#!/usr/bin/env python3
import sympy
from sympy.physics.quantum.cg import CG

S_half = sympy.Rational(1, 2)
memo_paths = {}
memo_csf = {}
a = sympy.Function('a')
b = sympy.Function('b')

def sort_spin_functions(expr):
    if expr.is_Add:
        sorted_terms = [sort_spin_functions(term) for term in expr.args]
        return sympy.Add(*sorted_terms)

    if expr.is_Mul:
        coeff_parts = []
        spin_parts = []
        for factor in expr.args:
            if isinstance(factor, (a, b)):
                spin_parts.append(factor)
            else:
                coeff_parts.append(factor)

        spin_parts.sort(key=lambda f: f.args[0])

        sorted_term = sympy.Mul(*coeff_parts) * sympy.Mul(*spin_parts)
        return sorted_term

    return expr

def find_paths_recursive(k, current_S, N_target, S_target):
    if (k, current_S) in memo_paths:
        return memo_paths[(k, current_S)]

    if k == N_target:
        return [[S_target]] if current_S == S_target else []

    if not (0 <= current_S <= k / 2):
        return []

    paths = []

    sub_paths_up = find_paths_recursive(k + 1, current_S + S_half, N_target, S_target)
    for p in sub_paths_up:
        paths.append([current_S] + p)

    if current_S > 0:
        sub_paths_down = find_paths_recursive(k + 1, current_S - S_half, N_target, S_target)
        for p in sub_paths_down:
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
    c_beta = CG(S_parent, M + S_half, S_half, -S_half, S, M).doit()

    term_alpha = 0
    if c_alpha != 0:
        parent_csf_alpha = construct_csf(path_tuple[:-1], M - S_half)
        if parent_csf_alpha != 0:
            term_alpha = c_alpha * parent_csf_alpha * a(k)

    term_beta = 0
    if c_beta != 0:
        parent_csf_beta = construct_csf(path_tuple[:-1], M + S_half)
        if parent_csf_beta != 0:
            term_beta = c_beta * parent_csf_beta * b(k)

    result = sympy.expand(term_alpha + term_beta)
    memo_csf[(path_tuple, M)] = result
    return result

def generate_csfs(N, S, M):
    S_sym = sympy.sympify(S)
    M_sym = sympy.sympify(M)

    if S < 0 or N < 0 or (N % 2 != (2*S_sym) % 2) or abs(M_sym) > S_sym:
        print("Invalid (N, S, M) combination.")
        return

    memo_paths.clear()
    memo_csf.clear()
    all_paths = find_paths_recursive(0, 0, N, S_sym)

    if not all_paths:
        print(f"No CSFs are possible for N={N}, S={S}.")
        return

    print(f"Found {len(all_paths)} CSFs for N={N}, S={S}, M={M}\n")
    sympy.init_printing(use_unicode=True)

    for i, path in enumerate(all_paths):
        header = f"--- CSF #{i+1} (Path: {path}) ---"
        print(header)
        csf = construct_csf(path, M_sym)
        if csf == 0:
            print(" (This CSF is zero for the given M value)")
        else:
            sorted_csf = sort_spin_functions(csf)
            simplified_csf = sympy.simplify(sorted_csf)
            sympy.pprint(simplified_csf)
        print("-" * len(header), "\n")


if __name__ == '__main__':
    target_N = 4
    target_S = 0
    target_M = 0

    generate_csfs(target_N, target_S, target_M)
