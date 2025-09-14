#--- balancer (homogeneous linear system solver) ---
from backend.core import parser
from fractions import Fraction
from math import gcd
from functools import reduce

def balance_equation(left_species, right_species):
    """
    Given lists of species formula strings on left and right, return integer coefficient lists.
    Example: left_species=['Zn','CuSO4'], right_species=['ZnSO4','Cu'] -> returns ([1,1],[1,1])
    Implementation: build element conservation matrix and find smallest integer nullspace vector.
    """
    species = left_species + right_species
    parsed = [parser.parse_formula(sp)[1] for sp in species]
    # unique elements
    elements = sorted({el for d in parsed for el in d.keys()})
    # Build matrix: rows elements, columns species. Left side positive, right side negative.
    matrix = []
    for el in elements:
        row = []
        for i, comp in enumerate(parsed):
            coeff = comp.get(el,0)
            # left species positive, right negative
            if i >= len(left_species):
                coeff = -coeff
            row.append(Fraction(coeff))
        matrix.append(row)
    # Solve for nullspace vector x (non-zero) such that M x = 0
    # We'll perform Gaussian elimination to RREF and parameterize free variables
    m = len(matrix)   # rows
    n = len(matrix[0]) if m>0 else 0  # cols
    # convert to augmented matrix copy
    A = [row[:] for row in matrix]  # m x n Fractions
    # Row-reduction to row-echelon form (not full RREF)
    row = 0
    pivot_cols = []
    for col in range(n):
        if row >= m:
            break
        # find pivot
        sel = None
        for r in range(row, m):
            if A[r][col] != 0:
                sel = r; break
        if sel is None:
            continue
        # swap
        if sel != row:
            A[row], A[sel] = A[sel], A[row]
        # normalize pivot row
        pivot = A[row][col]
        A[row] = [v / pivot for v in A[row]]
        # eliminate below
        for r in range(m):
            if r != row and A[r][col] != 0:
                factor = A[r][col]
                A[r] = [A[r][c] - factor*A[row][c] for c in range(n)]
        pivot_cols.append(col)
        row += 1
    # free columns are those not pivot columns
    free_cols = [c for c in range(n) if c not in pivot_cols]
    if not free_cols:
        # Only trivial solution; fall back to set last variable = 1 and solve (if possible)
        free_cols = [n-1]
    # parametrize: set each free var to a symbolic parameter; we'll choose 1 for the last free var, 0 for others,
    # then backsolve for pivot variables.
    params = {c: Fraction(0) for c in free_cols}
    params[free_cols[-1]] = Fraction(1)
    # backsolve for pivot vars by expressing them in terms of params
    sol = [Fraction(0) for _ in range(n)]
    # For each pivot row, find its pivot col and compute variable as negative sum of (coeff*param)
    for r in range(m):
        # find pivot col in this row (first non-zero)
        pivot_col = None
        for c in range(n):
            if A[r][c] == 1:
                pivot_col = c; break
            if A[r][c] != 0 and abs(A[r][c]) != 1:
                # not strictly RREF; but above elimination tried to go toward RREF
                pass
        if pivot_col is None:
            continue
        total = Fraction(0)
        for c in free_cols:
            total += A[r][c] * params[c]
        sol[pivot_col] = -total
    # set free vars
    for c in free_cols:
        sol[c] = params[c]
    # sol is rational; scale to smallest integers
    dens = [fr.denominator for fr in sol]
    lcm_denom = 1
    for d in dens:
        lcm_denom = lcm_denom * d // gcd(lcm_denom, d)
    int_sol = [int(fr * lcm_denom) for fr in sol]
    # ensure all are non-negative; if all negative, flip sign
    if all(x <= 0 for x in int_sol):
        int_sol = [-x for x in int_sol]
    # reduce by gcd
    g = reduce(gcd, [abs(x) for x in int_sol if x!=0], 1)
    int_sol = [x//g for x in int_sol]
    left_coeffs = int_sol[:len(left_species)]
    right_coeffs = int_sol[len(left_species):]
    return left_coeffs, right_coeffs
