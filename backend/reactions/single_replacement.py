# --- Single Replacement Logic ---
# Predicts products for single-replacement reactions:
#   - metal displaces metal
#   - metal displaces acid
#   - metal displaces water
#   - halogen displaces halogen
#
# Flow:
#   1. Check if reaction is possible (activity series / halogen order).
#   2. Build product formulas (using charge inference + formula builder).
#   3. Balance equation with Gaussian elimination (fractions).
#
# Notes:
#   - Limited to common polyatomic ions and charge heuristics.
#   - Transition metals with multiple oxidation states not fully handled.
#   - Oxidizing-acid exceptions as HNO3 are out of scope.

from backend.core import balancer, charges, parser, rules, utils
import re


def is_halogen(symbol: str):
    """Return True if the symbol is a halogen in HALOGEN_ORDER."""
    return symbol in rules.HALOGEN_ORDER


def is_in_activity_series(symbol: str):
    """Return True if the symbol is present in the metal activity series."""
    return symbol in rules.ACTIVITY_SERIES


def can_perform_single_replacement(element_raw: str, compound_raw: str):
    """
    Decide if single-replacement reaction is possible.
    Returns (possible: bool, subtype: str, details/reason).
    Subtypes: halogen | metal_displaces_metal | metal_displaces_hydrogen | metal_displaces_water
    """
    a_raw = element_raw.replace(" ", "")
    b_raw = compound_raw.replace(" ", "")

    # Verify first reactant is a single element
    _, el_counts = parser.parse_formula(a_raw)
    if len(el_counts) != 1:
        return False, None, "Reactant is not a single element"
    el_symbol = next(iter(el_counts.keys()))

    # --- Halogen displacement case ---
    if is_halogen(el_symbol):
        cation, anion = parser.split_cation_anion(b_raw)
        if anion == "":
            return False, "halogen", f"Compound '{b_raw}' has no anion to displace."

        # Detect halogen anion in compound
        found, key, _, _, _, pos = parser.detect_polyatomic_in_formula(b_raw)
        if found and pos == 'suffix':
            a_detect = key
        else:
            a_detect = next((sym for sym in parser.ELEMENT_SYMBOLS if b_raw.endswith(sym)), None)

        if a_detect is None:
            return False, "halogen", f"Could not identify halide anion in {b_raw}."

        if el_symbol not in rules.HALOGEN_ORDER or a_detect not in rules.HALOGEN_ORDER:
            return False, "halogen", f"{el_symbol} or {a_detect} not recognized as halogen."

        if rules.HALOGEN_ORDER.index(el_symbol) <= rules.HALOGEN_ORDER.index(a_detect):
            return True, "halogen", {"incoming": el_symbol, "replaced_anion": a_detect}
        return False, "halogen", f"{el_symbol} is less reactive than {a_detect}; no reaction."

    # --- Metal/Hydrogen/Water displacement cases ---
    if el_symbol == "H":
        return False, None, "Free hydrogen atoms not considered replacers."

    if not is_in_activity_series(el_symbol):
        return False, "metal", f"{el_symbol} not in activity series."

    # Acid case
    if b_raw.startswith("H") and b_raw != "H2O":
        if rules.ACTIVITY_SERIES.index(el_symbol) <= rules.ACTIVITY_SERIES.index("H"):
            return True, "metal_displaces_hydrogen", {"incoming": el_symbol, "acid": b_raw}
        return False, "metal_displaces_hydrogen", f"{el_symbol} is below hydrogen in activity series."

    # Water case
    if b_raw == "H2O":
        reactive_with_cold_water = {"Li","Na","K","Rb","Cs","Ca","Sr","Ba"}
        if el_symbol in reactive_with_cold_water:
            return True, "metal_displaces_water", {"incoming": el_symbol, "target": b_raw}
        return False, "metal_displaces_water", f"{el_symbol} does not react with cold water."

    # Salt case
    cation, anion = parser.split_cation_anion(b_raw)
    if anion == "":
        return False, "metal", f"{b_raw} is not an ionic salt or acid."
    if cation not in rules.ACTIVITY_SERIES:
        return False, "metal", f"Cation '{cation}' in '{b_raw}' not found in activity series."

    if rules.ACTIVITY_SERIES.index(el_symbol) <= rules.ACTIVITY_SERIES.index(cation):
        return True, "metal_displaces_metal", {"incoming": el_symbol, "replaced_cation": cation, "anion": anion}
    return False, "metal_displaces_metal", f"{el_symbol} is less reactive than {cation}; no reaction."


def predict_single_replacement(reactant_raw: str, compound_raw: str):
    """
    Predict products for a single-replacement reaction (if possible).
    Returns dict with keys:
        possible: bool
        reason: str (if not possible)
        products: [list of str]
        balanced_equation: str
        subtype: str
    """
    possible, subtype, details = can_perform_single_replacement(reactant_raw, compound_raw)
    if not possible:
        return {"possible": False, "reason": details}

    _, el_counts = parser.parse_formula(reactant_raw)
    el_symbol = next(iter(el_counts.keys()))
    left_species = [reactant_raw, compound_raw]
    products, right_list = [], []

    # --- Build products ---
    if subtype == "halogen":
        cation, _ = parser.split_cation_anion(compound_raw)
        incoming = details["incoming"]
        try:
            cation_charge = charges.infer_cation_charge(cation)
        except KeyError as e:
            return {"possible": False, "reason": str(e)}
        new_salt = utils.formula_from_ions(cation, cation_charge, incoming, -1)
        displaced = details["replaced_anion"] + "2"
        products, right_list = [new_salt, displaced], [new_salt, displaced]

    elif subtype == "metal_displaces_hydrogen":
        cation = el_symbol
        anion = re.sub(r"^H\d*", "", compound_raw)  # remove leading H/Hn
        try:
            c_charge = charges.infer_cation_charge(cation)
            a_charge = charges.infer_anion_charge(anion)
        except KeyError as e:
            return {"possible": False, "reason": str(e)}
        salt = utils.formula_from_ions(cation, c_charge, anion, a_charge)
        products, right_list = [salt, "H2"], [salt, "H2"]

    elif subtype == "metal_displaces_water":
        cation = el_symbol
        try:
            c_charge = charges.infer_cation_charge(cation)
        except KeyError as e:
            return {"possible": False, "reason": str(e)}
        hydroxide = utils.formula_from_ions(cation, c_charge, "OH", -1)
        products, right_list = [hydroxide, "H2"], [hydroxide, "H2"]

    elif subtype == "metal_displaces_metal":
        incoming, replaced, anion = details["incoming"], details["replaced_cation"], details["anion"]
        try:
            c_charge = charges.infer_cation_charge(incoming)
            a_charge = charges.infer_anion_charge(anion)
            salt = utils.formula_from_ions(incoming, c_charge, anion, a_charge)
        except KeyError as e:
            return {"possible": False, "reason": str(e)}
        products, right_list = [salt, replaced], [salt, replaced]

    else:
        return {"possible": False, "reason": f"Unhandled subtype {subtype}"}

    # --- Balance ---
    try:
        left_coeffs, right_coeffs = balancer.balance_equation(left_species, right_list)
        def fmt_side(species, coeffs):
            return " + ".join(f"{c} {s}" if c != 1 else s for c, s in zip(coeffs, species))
        balanced = fmt_side(left_species, left_coeffs) + " -> " + fmt_side(right_list, right_coeffs)
    except Exception as e:
        return {"possible": True, "products": products, "balanced_equation": None,
                "warning": f"Balancing failed: {e}"}

    return {"possible": True, "products": products, "balanced_equation": balanced,
            "subtype": subtype, "details": details}
