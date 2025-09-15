#--- singleR logic ---
# - Predicts products for single-replacement reactions (metal/halogen/hydrogen cases)
# - Builds formulas for predicted ionic products
# - Balances the resulting equation (pure-Python Gaussian elimination with Fractions)
# - Works on a broad set of *common* species; has limitations and will warn when it cannot decide.
#
# Limitations (important):
# - Uses an explicit list of common polyatomic ions and element group heuristics.
# - Not exhaustive for all elements/oxidation states (transition metals with multiple states may be ambiguous).
# - Does not model oxidizing-acid exceptions (e.g., concentrated HNO3 behavior); it flags such cases.


from backend.core import balancer, charges, parser, rules, utils
import re


def is_halogen(symbol: str):
    return symbol in rules.HALOGEN_ORDER

def is_in_activity_series(symbol: str):
    return symbol in rules.ACTIVITY_SERIES

def can_perform_single_replacement(element_raw: str, compound_raw: str):
    """
    Decide if single-replacement reaction possible and what subcase it is.
    Returns (possible: bool, subtype: 'metal'|'halogen'|'hydrogen', details dict or reason string)
    """
    a_raw = element_raw.replace(" ", "")
    b_raw = compound_raw.replace(" ", "")
    # parse element symbol (could be 'Cl2' or 'O2'): get symbol of element
    _, el_counts = parser.parse_formula(a_raw)
    if len(el_counts) != 1:
        return False, None, "Reactant is not a single element"
    el_symbol = next(iter(el_counts.keys()))
    # determine categories
    if is_halogen(el_symbol):
        # halogen replacement: must find a halide anion in compound
        # split compound cation/anion
        cation, anion = parser.split_cation_anion(b_raw)
        # anion may be multi-part; try to canonicalize anion
        # if anion empty -> compound looks like single element -> NR for halogen
        if anion == "":
            return False, "halogen", f"Compound '{b_raw}' is not ionic/does not contain an anion to displace."
        # remove numeric suffixes for matching (e.g., Br in NaBr)
        # attempt to detect anion symbol using polyatomic mapping or element prefix
        a_detect = None
        # polyatomic end match
        found, key, comp, charge, name, pos = parser.detect_polyatomic_in_formula(b_raw)
        if found and pos=='suffix':
            a_detect = key
        else:
            # try element single-letter/triple match at end
            for sym in parser.ELEMENT_SYMBOLS:
                if b_raw.endswith(sym):
                    a_detect = sym; break
        if a_detect is None:
            return False, "halogen", f"Could not identify anion in {b_raw}."
        # now check order
        if el_symbol not in rules.HALOGEN_ORDER or a_detect not in rules.HALOGEN_ORDER:
            return False, "halogen", f"Either {el_symbol} or {a_detect} not recognized as a halogen in our table."
        if rules.HALOGEN_ORDER.index(el_symbol) <= rules.HALOGEN_ORDER.index(a_detect):
            # lower index => more reactive -> can replace
            return True, "halogen", {"incoming":el_symbol, "replaced_anion":a_detect}
        else:
            return False, "halogen", f"{el_symbol} is less reactive than {a_detect}; no reaction."
    else:
        # assume metal/hydrogen case (we treat hydrogen specially)
        # If element is H -> hydrogen replacement (acid)
        if el_symbol == "H":
            # Hydrogen atom (unlikely as free element) - not typical case
            return False, None, "Free hydrogen atoms are not handled as replacers."
        # determine if element is in activity series (metal)
        if not is_in_activity_series(el_symbol):
            return False, "metal", f"{el_symbol} not in activity series (unknown reactivity)"
        # classify compound: is it an acid (starts with H), a salt (contains metal cation), or water?
        if b_raw.startswith("H") and b_raw != "H2O":
            # acid case - el_symbol must be above H in activity series
            if rules.ACTIVITY_SERIES.index(el_symbol) <= rules.ACTIVITY_SERIES.index("H"):
                return True, "metal_displaces_hydrogen", {"incoming": el_symbol, "acid": b_raw}
            else:
                return False, "metal_displaces_hydrogen", f"{el_symbol} is below hydrogen in activity series; won't produce H2."
        if b_raw == "H2O":
            # metal + water -> hydroxide + H2 for reactive metals (group1 and some group2)
            reactive_with_cold_water = {"Li","Na","K","Rb","Cs","Ca","Sr","Ba"}
            if el_symbol in reactive_with_cold_water:
                return True, "metal_displaces_water", {"incoming": el_symbol, "target": b_raw}
            else:
                return False, "metal_displaces_water", f"{el_symbol} does not react with cold water."
        # else assume salt -> try detect cation in compound
        cation, anion = parser.split_cation_anion(b_raw)
        # If cation equals compound (no anion) -> not a salt
        if anion == "":
            return False, "metal", f"{b_raw} is not an ionic salt or acid."
        # check cation presence in activity series
        if cation not in rules.ACTIVITY_SERIES:
            # maybe cation is polyatomic or ammonium; assume metal replacement cannot proceed unless cation is a metal
            # but if cation is NH4, reaction becomes ammonia-producing? out of scope
            return False, "metal", f"Cation '{cation}' in '{b_raw}' not found in activity series."
        # compare activity
        if rules.ACTIVITY_SERIES.index(el_symbol) <= rules.ACTIVITY_SERIES.index(cation):
            return True, "metal_displaces_metal", {"incoming": el_symbol, "replaced_cation": cation, "anion": anion}
        else:
            return False, "metal_displaces_metal", f"{el_symbol} is less reactive than {cation}; no reaction."

def predict_single_replacement(reactant_raw: str, compound_raw: str):
    """
    Predict products for a single-replacement reaction (if possible).
    Returns dict with keys: possible(bool), reason, products(list of strings), balanced_equation(str)
    """
    possible, subtype, details = can_perform_single_replacement(reactant_raw, compound_raw)
    if not possible:
        return {"possible": False, "reason": details}
    # now build products according to subtype
    _, el_counts = parser.parse_formula(reactant_raw)
    el_symbol = next(iter(el_counts.keys()))
    left_species = [reactant_raw, compound_raw]
    products = []
    if subtype == "halogen":
        incoming = details["incoming"]
        # identify anion in compound (to be replaced)
        # split compound into cation and anion string
        cation, anion = parser.split_cation_anion(compound_raw)
        # predicted salt: cation + incoming_anion
        try:
            incoming_anion_charge = charges.infer_anion_charge(incoming)
        except KeyError:
            # halogen as anion is simple: charge -1
            incoming_anion_charge = -1
        try:
            cation_charge = charges.infer_cation_charge(cation)
        except KeyError as e:
            return {"possible": False, "reason": str(e)}
        new_salt = utils.formula_from_ions(cation, cation_charge, incoming, incoming_anion_charge)
        # displaced species is halogen diatomic (Y2)
        displaced = details["replaced_anion"] + "2" if len(details["replaced_anion"])==1 or details["replaced_anion"] in rules.HALOGEN_ORDER else details["replaced_anion"] + "2"
        products = [new_salt, displaced]
        right_list = [new_salt, displaced]
    elif subtype == "metal_displaces_hydrogen":
        # metal + acid -> salt + H2
        cation = el_symbol
        '''
        # get conjugate base (anion) of the acid: remove leading H and parse remainder
        acid = compound_raw
        anion_part = acid[1:]
        if anion_part == "":  # e.g., "H" only
            return {"possible": False, "reason": f"Acid '{acid}' malformed or unsupported."}
        anion = anion_part
        '''
        # strip all leading H with optional digit
        anion = re.sub(r"^H\d*", "", compound_raw)
        try:
            c_charge = charges.infer_cation_charge(cation)
            a_charge = charges.infer_anion_charge(anion)
        except KeyError as e:
            return {"possible": False, "reason": str(e)}
        salt = utils.formula_from_ions(cation, c_charge, anion, a_charge)
        displaced = "H2"
        products = [salt, displaced]
        right_list = [salt, displaced]
    elif subtype == "metal_displaces_water":
        # highly reactive metals + water -> metal hydroxide + H2
        cation = el_symbol
        try:
            c_charge = charges.infer_cation_charge(cation)
        except KeyError as e:
            return {"possible": False, "reason": str(e)}
        # anion is OH with charge -1
        a_charge = -1
        hydroxide = utils.formula_from_ions(cation, c_charge, "OH", a_charge)
        products = [hydroxide, "H2"]
        right_list = [hydroxide, "H2"]
    elif subtype == "metal_displaces_metal":
        incoming = details["incoming"]
        replaced = details["replaced_cation"]
        anion = details["anion"]
        # build incoming salt (incoming + anion)
        try:
            c_charge = charges.infer_cation_charge(incoming)
            a_charge = charges.infer_anion_charge(anion)
            salt = utils.formula_from_ions(incoming, c_charge, anion, a_charge)
        except KeyError as e:
            return {"possible": False, "reason": str(e)}
        displaced = replaced  # elemental metal
        products = [salt, displaced]
        right_list = [salt, displaced]
    else:
        return {"possible": False, "reason": f"Unhandled subtype {subtype}"}

    # Balance the equation
    try:
        left_coeffs, right_coeffs = balancer.balance_equation(left_species, right_list)
        # Format balanced equation string
        def fmt_side(species, coeffs):
            parts = []
            for c, s in zip(coeffs, species):
                if c == 1:
                    parts.append(s)
                else:
                    parts.append(f"{c} {s}")
            return " + ".join(parts)
        balanced = fmt_side(left_species, left_coeffs) + " -> " + fmt_side(right_list, right_coeffs)
    except Exception as e:
        return {"possible": True, "products": products, "balanced_equation": None, "warning": f"Balancing failed: {e}"}

    return {"possible": True, "products": products, "balanced_equation": balanced, "subtype": subtype, "details": details}
