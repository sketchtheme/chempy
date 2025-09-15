from backend.reactions import single_replacement as SR
from backend.core import parser, charges, utils
import re

tests = [
    # --- Metal displaces metal ---
    ("Zn", "CuSO4"),       # classic: Zn more reactive than Cu
    ("Fe", "CuSO4"),       # Fe above Cu
    ("Ag", "CuSO4"),       # Ag below Cu → no reaction
    ("Mg", "FeCl2"),       # Mg above Fe
    ("Pb", "ZnSO4"),       # Pb below Zn → no reaction
    ("Ca", "Cu(OH)2"),     # Ca above Cu → hydroxide displacement

    # --- Metal displaces hydrogen from acid ---
    ("Zn", "HCl"),         # Zn above H
    ("Mg", "H2SO4"),       # Mg above H
    ("Zn", "H3PO4"),       # polyatomic acid case
    ("Cu", "HCl"),         # Cu below H → no reaction
    ("Hg", "HCl"),         # Hg below H → no reaction

    # --- Metal displaces hydrogen from water ---
    ("K", "H2O"),          # group 1 alkali → reacts
    ("Ca", "H2O"),         # group 2 alkaline earth → reacts
    ("Fe", "H2O"),         # Fe does not react with cold water
    ("Mg", "H2O"),         # Mg does not react with cold water

    # --- Halogen replacement ---
    ("Cl2", "NaBr"),       # Cl more reactive than Br
    ("Br2", "KI"),         # Br more reactive than I
    ("I2", "NaCl"),        # I less reactive than Cl → no reaction
    ("Cl2", "NaF"),        # Cl less reactive than F → no reaction

    # --- Edge / tricky cases ---
    ("H2", "CuSO4"),       # free H2 molecule → not handled as displacer
    ("Na", "NaCl"),        # same element with salt → no net reaction
    ("Al", "Cu(NO3)2"),    # polyatomic nitrate with transition metal
    ("Ni", "Pb(NO3)2"),    # Ni vs Pb, nitrate salt
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
    #b_norm = normalize_compound_input(b)
    out = SR.predict_single_replacement(a, b) #b_norm
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
