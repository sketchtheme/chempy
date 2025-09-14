#--- charges ---
POLYATOMIC = {
    # polyatomic ions (composition dict, charge, name)
    "NH4": ({"N":1,"H":4}, +1, "ammonium"),
    "NO3": ({"N":1,"O":3}, -1, "nitrate"),
    "SO4": ({"S":1,"O":4}, -2, "sulfate"),
    "CO3": ({"C":1,"O":3}, -2, "carbonate"),
    "PO4": ({"P":1,"O":4}, -3, "phosphate"),
    "OH":  ({"O":1,"H":1}, -1, "hydroxide"),
    "CH3COO": ({"C":2,"H":3,"O":2}, -1, "acetate"),
    "NO2": ({"N":1,"O":2}, -1, "nitrite"),
    "ClO3": ({"Cl":1,"O":3}, -1, "chlorate"),
}
COMMON_CATION_CHARGES = {
    # explicit ionic charges for cations
    "Li": 1, "Na": 1, "K": 1, "Rb": 1, "Cs": 1,
    "Be": 2, "Mg": 2, "Ca": 2, "Sr": 2, "Ba": 2,
    "Al": 3,
    "Zn": 2, "Mn": 2, "Fe": 2, "Co": 2, "Ni": 2,
    "Cu": 2, "Ag": 1, "Sn": 2, "Pb": 2,
    "H": 1,
    "NH4": 1
}
COMMON_ANION_CHARGES = {
    # monoatomic or recognized anion charges
    "F": -1, "Cl": -1, "Br": -1, "I": -1,
    "O": -2, "S": -2, "N": -3,
    "OH": -1, "NO3": -1, "SO4": -2, "CO3": -2, "PO4": -3, "CH3COO": -1
}

from backend.core import parser
from math import gcd
from functools import reduce

#charge inference
def infer_cation_charge(cation_str: str):
    """
    Infer integer positive charge of a cation using:
      1. Explicit map (COMMON_CATION_CHARGES)
      2. POLYATOMIC map
      3. Group-based heuristics for predictable elements
    Returns None if charge cannot be inferred safely.
    """

    # 1. direct mapping
    if cation_str in COMMON_CATION_CHARGES:
        return COMMON_CATION_CHARGES[cation_str]

    # 2. polyatomic lookup
    if cation_str in POLYATOMIC:
        comp, charge, name = POLYATOMIC[cation_str]
        if charge > 0:
            return charge

    # 3. periodic group heuristics
    group1 = {"H","Li","Na","K","Rb","Cs","Fr"} # always +1
    group2 = {"Be","Mg","Ca","Sr","Ba","Ra"} # always +2
    group13 = {"B","Al","Ga","In","Tl"} # mostly +3, but Tl can also be +1
    group14 = {"C","Si","Ge","Sn","Pb"} # +4 common, but Sn/Pb also +2
    group15 = {"N","P","As","Sb","Bi"} # +3 common, +5 also possible
    transition_common = {"Zn","Cd","Hg"} # reliably +2

    if cation_str in group1:
        return 1
    if cation_str in group2:
        return 2
    if cation_str in group13:
        # fallback: Tl is special (+1), others mostly +3
        return 1 if cation_str == "Tl" else 3
    if cation_str in group14:
        # Sn/Pb flexible, default to +2 for stability
        return 2 if cation_str in {"Sn","Pb"} else 4
    if cation_str in group15:
        # common low oxidation state
        return 3
    if cation_str in transition_common:
        return 2

    # 4. unknown / ambiguous (most transition metals fall here)
    return None

def infer_anion_charge(anion_str: str):
    """
    Return integer negative charge for anion_str using COMMON_ANION_CHARGES or POLYATOMIC mapping heuristics.
    """
    if anion_str in COMMON_ANION_CHARGES:
        return COMMON_ANION_CHARGES[anion_str]
    if anion_str in POLYATOMIC:
        comp, charge, name = POLYATOMIC[anion_str]
        return charge
    # anion may be a single element (like Cl)
    if anion_str in parser.ELEMENT_SYMBOLS:
        # halogens -> -1
        if anion_str in {"F","Cl","Br","I"}:
            return -1
        # oxygen -> -2
        if anion_str == "O":
            return -2
        # sulfur -> -2
        if anion_str == "S":
            return -2
    # can't deduce
    raise KeyError(f"Unknown anion charge for '{anion_str}' — expand COMMON_ANION_CHARGES or POLYATOMIC")
