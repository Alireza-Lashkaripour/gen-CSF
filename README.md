# gen‑CSF
Spin configuration state function calculator

## Overview  
`gen‑CSF` computes spin‐adapted Configuration State Functions (CSFs) for N open‑shell electrons with total spin S and projection M, via recursive Clebsch–Gordan formulas.

- **Compute microstates & multiplets**  
  - Enter **N** to see total microstates (2^N) and a list of available spin multiplets (Singlet, Triplet, etc.).
- **Visualize distribution**  
  - Displays an ASCII “bubble” plot of spin-multiplet counts vs. total spin S.
- **Interactive CSF generation**  
  - After listing, pick **S** and **Mₛ** to automatically generate all Configuration State Functions via Clebsch–Gordan recursion.
- **Flexible workflow**  
  - Fully command-line driven; no additional arguments or configuration files needed.


## Installation & Usage  
```bash
git clone https://github.com/yourusername/gen‑CSF.git
cd gen‑CSF
python3 csf_wrapper.py
```  
1. Enter **N** (number of open‑shell electrons)  
2. View total microstates and available spin multiplets  
3. Select **S** and **M_s** to generate CSFs  

## Theory  
CSFs are built by successive spin coupling:

### Spin Addition (S → S + ½)  
$$
X\bigl(N,\,S+\tfrac12,\,M+\tfrac12\bigr)
=\frac{\sqrt{S+M+1}\;X(N-1,S,M)\,\alpha(N)
+\sqrt{S-M}\;X(N-1,S,M+1)\,\beta(N)}
{\sqrt{2S+1}}
$$

### Spin Subtraction (S → S – ½)  
$$
X\bigl(N,\,S-\tfrac12,\,M+\tfrac12\bigr)
=\frac{-\sqrt{S-M}\;X(N-1,S,M)\,\alpha(N)
+\sqrt{S+M+1}\;X(N-1,S,M+1)\,\beta(N)}
{\sqrt{2S+1}}
$$

## Files  
- `csf_generator.py`: core CSF routines  
- `csf_wrapper.py`: command‑line interface  

