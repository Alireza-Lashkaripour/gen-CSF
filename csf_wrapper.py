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
    while True:
        S_choice = float(input("\nPick a total spin S from above list: "))
        if S_choice in mults:
            break
        print("Invalid S, try again.")
    while True:
        M_choice = float(input("Pick M_s (|M_s| ≤ S, half-integer): "))
        if abs(M_choice) <= S_choice and (2*M_choice).is_integer():
            break
        print("Invalid M_s, try again.")
    print(f"\n=== Generating CSFs for N={N}, S={S_choice}, M_s={M_choice} ===\n")
    generate_csfs(N, S_choice, M_choice)

if __name__ == "__main__":
    main()

