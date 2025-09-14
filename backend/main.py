from backend.reactions import single_replacement as SR
import re

tests = [
#    ("Zn", "CuSO4"),
#    ("Fe", "CuSO4"),
#    ("Ag", "HCl"),
#    ("Cl2", "2 NaBr"),  # raw string; splitter will see '2NaBr' as formula - balancing handles numeric prefixes
    ("Ca", "H2O"),
#    ("Zn", "HCl"),
    
    # --- metal displaces metal ---
    ("Mg", "FeCl2"),       # should work
#    ("Pb", "ZnSO4"),       # no reaction
    ("Al", "Cu(NO3)2"),    # should work

    # --- metal displaces water ---
#    ("K", "H2O"),          # should work
#    ("Fe", "H2O"),         # no reaction (cold water)

    # --- metal displaces hydrogen (acids) ---
    ("Mg", "H2SO4"),       # should work
#    ("Cu", "H2SO4"),       # no reaction

    # --- halogen displacement ---
#    ("Br2", "KI"),         # should work
#    ("I2", "NaCl"),        # no reaction
#    ("Cl2", "NaF"),        # no reaction

    # --- polyatomic / tricky ---
    ("Zn", "H3PO4"),       # Zn3(PO4)2 + H2
    ("Ca", "Cu(OH)2"),     # Ca(OH)2 + Cu
    ("Ni", "Pb(NO3)2"),    # Ni(NO3)2 + Pb
#    ("Hg", "HCl"),         # no reaction
]


def normalize_compound_input(raw: str):
    """Strip spaces and numeric coefficients in front of formulas for this predictor (we handle 1 stoichiometric unit)."""
    r = raw.replace(" ", "")
    # remove leading coefficient if like '2NaBr' -> 'NaBr' (we predict per formula unit now)
    m = re.match(r'^(\d+)([A-Za-z\(\)0-9]+)$', r)
    if m:
        return m.group(2)
    return r

for a, b in tests:
    b_norm = normalize_compound_input(b)
    out = SR.predict_single_replacement(a, b_norm)
    print("====")
    print(f"Reactants: {a} + {b}")
    if not out["possible"]:
        print("No reaction:", out.get("reason"))
    else:
        print("Predicted products:", out["products"])
        print("Subtype:", out.get("subtype"))
        print("Balanced:", out.get("balanced_equation"))
        if "warning" in out:
            print("Warning:", out["warning"])
