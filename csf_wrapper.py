#!/usr/bin/env python3
import sympy
from csf_generator import generate_csfs

def compute_spin_multiplets(N):
    total = 2**N
    start = 0 if N % 2 == 0 else sympy.Rational(1, 2)
    S_max = sympy.Rational(N, 2)
    counts = {}
    S = start
    while S <= S_max:
        k = sympy.Rational(N, 2) + S
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

def possible_Ms(S):
    return [-S + i for i in range(int(2*S) + 1)]

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
        Ms_list = possible_Ms(S)
        formatted = ', '.join(f"{M:.1f}" for M in Ms_list)
        print(f"   S={S:g}: M_s ∈ {{ {formatted} }}")
    while True:
        S_choice = float(input("\nPick a total spin S from above list: "))
        if S_choice in mults:
            break
        print("Invalid S, try again.")
    while True:
        M_choice = float(input("Pick M_s from the list above: "))
        if M_choice in possible_Ms(S_choice):
            break
        print("Invalid M_s, try again.")
    print(f"\n=== Generating CSFs for N={N}, S={S_choice}, M_s={M_choice} ===\n")
    generate_csfs(N, S_choice, M_choice)

if __name__ == "__main__":
    main()

