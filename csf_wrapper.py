#!/usr/bin/env python3
import sympy
from csf_generator import a, b, find_paths_recursive, construct_csf, memo_paths, memo_csf
from sympy import pprint

def compute_spin_multiplets(N):
    total = 2**N
    start = 0 if N % 2 == 0 else sympy.Rational(1, 2)
    S_max = sympy.Rational(N, 2)
    counts = {}
    S = start
    while S <= S_max:
        k  = sympy.Rational(N, 2) + S
        d1 = sympy.binomial(N, int(k))
        d2 = sympy.binomial(N, int(k + 1))
        cnt = int(d1 - d2)
        if cnt > 0:
            counts[float(S)] = cnt
        S += 1
    return total, counts

def name_for_multiplicity(m):
    mnames = {
        1: "Singlet", 2: "Doublet", 3: "Triplet", 4: "Quartet",
        5: "Quintet", 6: "Sextet", 7: "Septet", 8: "Octet"
    }
    return mnames.get(m, f"{m}-plet")

def print_text_plot(N, mults):
    S_vals = sorted(mults.keys(), reverse=True)
    max_count = max(mults.values())
    label_width = max(len(f"{S:g}") for S in S_vals)
    for S in S_vals:
        label = f"{S:g}".rjust(label_width)
        bubbles = '●' * mults[S]
        print(f"{label} │ {bubbles}")
    axis = ' ' * (label_width + 1) + '└' + '─' * max_count
    print(axis + f" N={N}")

def sort_spin_functions(expr):
    if expr.is_Add:
        return sympy.Add(*[sort_spin_functions(term) for term in expr.args])
    if expr.is_Mul:
        parts = [sort_spin_functions(f) for f in expr.args]
        coeffs, spins = [], []
        for f in parts:
            if f.func in (a, b):
                spins.append(f)
            else:
                coeffs.append(f)
        spins.sort(key=lambda f: f.args[0])
        return sympy.Mul(*coeffs) * sympy.Mul(*spins)
    return expr

def main():
    N = int(input("Enter number of open-shell electrons N: "))
    total, mults = compute_spin_multiplets(N)

    print(f"\n→ Total microstates = 2^{N} = {total}\n")
    print("→ Unique spin multiplets:")
    for S, cnt in sorted(mults.items(), key=lambda x: -x[0]):
        m = int(2*S + 1)
        name = name_for_multiplicity(m)
        pl = "s" if cnt > 1 else ""
        print(f"   {cnt} {name}{pl}  (S={S}, multiplicity={m})")

    print("\n→ Spin multiplets distribution:")
    print_text_plot(N, mults)

    print("\n→ Possible M_s (spin projection quantum number) for each S:")
    for S in sorted(mults.keys(), reverse=True):
        Ms = [-S + i for i in range(int(2*S) + 1)]
        formatted = ', '.join(f"{M:.1f}" for M in Ms)
        print(f"   S={S:g}: M_s ∈ {{ {formatted} }}")

    while True:
        S_choice = float(input("\nPick a total spin S from above list: "))
        if S_choice in mults:
            break
        print("Invalid S, try again.")
    while True:
        M_choice = float(input("Pick M_s from the list above: "))
        if abs(M_choice) <= S_choice and (2*M_choice).is_integer():
            break
        print("Invalid M_s, try again.")

    S_sym = sympy.Rational(int(2*S_choice), 2)
    M_sym = sympy.Rational(int(2*M_choice), 2)

    memo_paths.clear()
    memo_csf.clear()
    all_paths = find_paths_recursive(0, sympy.Rational(0), N, S_sym)

    if not all_paths:
        print(f"\nNo CSFs are possible for N={N}, S={S_sym}.")
        return

    print(f"\nFound {len(all_paths)} CSFs for N={N}, S={S_sym}, M={M_sym}\n")
    sympy.init_printing(use_unicode=True)

    for i, path in enumerate(all_paths, start=1):
        header = f"--- CSF #{i} (Path: {path}) ---"
        print(header)
        csf = construct_csf(path, M_sym)
        if csf == 0:
            print(" (This CSF is zero for the given M value)")
        else:
            sorted_csf = sort_spin_functions(csf)
            simplified = sympy.simplify(sorted_csf)
            pprint(simplified)
        print("-" * len(header), "\n")

if __name__ == "__main__":
    main()

