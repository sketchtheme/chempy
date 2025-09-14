#--- parsing ---
from backend.core import rules, charges
import re

ELEMENT_SYMBOLS = [
 "H","He","Li","Be","B","C","N","O","F","Ne","Na","Mg","Al","Si","P","S","Cl","Ar",
 "K","Ca","Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge","As","Se","Br","Kr",
 "Rb","Sr","Y","Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn","Sb","Te","I","Xe",
 "Cs","Ba","La","Ce","Pr","Nd","Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu",
 "Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg","Tl","Pb","Bi"
]
#longest-first order to match multi-letter symbols correctly
ELEMENT_SYMBOLS.sort(key=lambda s: -len(s))

'''
def parse_formula(formula: str):
    """
    Parse chemical formula into element counts, handling parentheses.
    Returns a dict: {element_symbol: count, ...}
    """
    # Tokenize into element symbols, parentheses, and numbers
    tokens = re.findall(r'([A-Z][a-z]?|\(|\)|\d+)', formula)
    stack = [{}]  # stack of dicts for parenthesis groups
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok == '(':
            stack.append({})
            i += 1
        elif tok == ')':
            group = stack.pop()
            i += 1
            # read multiplier if present
            mult = 1
            if i < len(tokens) and tokens[i].isdigit():
                mult = int(tokens[i]); i += 1
            # multiply and merge into top of stack
            for el, cnt in group.items():
                stack[-1][el] = stack[-1].get(el, 0) + cnt * mult
        elif re.match(r'\d+$', tok):
            # standalone number shouldn't appear normally; attach to previous element
            # but our tokenizer expects numbers only after elements or ')'; skip
            i += 1
        else:
            # element symbol
            el = tok
            cnt = 1
            # check next token for number
            if i+1 < len(tokens) and tokens[i+1].isdigit():
                cnt = int(tokens[i+1])
                i += 1
            stack[-1][el] = stack[-1].get(el, 0) + cnt
            i += 1
    if len(stack) != 1:
        raise ValueError("Unbalanced parentheses in formula: " + formula)
    return stack[0]
'''
def parse_formula(formula: str):
    """
    Parse chemical formula into both:
    - ordered list of (element/ion, count)
    - dict of element counts
    Handles parentheses.
    """
    tokens = re.findall(r'([A-Z][a-z]?|\(|\)|\d+)', formula)
    stack = [[[], {}]]  # each stack frame: [list, dict]
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok == '(':
            stack.append([[], {}])
            i += 1
        elif tok == ')':
            group_list, group_dict = stack.pop()
            i += 1
            mult = 1
            if i < len(tokens) and tokens[i].isdigit():
                mult = int(tokens[i]); i += 1
            # multiply counts and append to parent
            for sym, cnt in group_list:
                stack[-1][0].append((sym, cnt * mult))
            for el, cnt in group_dict.items():
                stack[-1][1][el] = stack[-1][1].get(el, 0) + cnt * mult
        elif re.match(r'\d+$', tok):
            # standalone number (shouldn’t happen if regex is correct)
            i += 1
        else:
            # element or ion symbol
            el = tok
            cnt = 1
            if i+1 < len(tokens) and tokens[i+1].isdigit():
                cnt = int(tokens[i+1])
                i += 1
            stack[-1][0].append((el, cnt))
            stack[-1][1][el] = stack[-1][1].get(el, 0) + cnt
            i += 1
    if len(stack) != 1:
        raise ValueError("Unbalanced parentheses in formula: " + formula)
    return stack[0][0], stack[0][1]  # (ordered list, dict)


#--- cation/anion detection helpers ---

def detect_polyatomic_in_formula(raw: str):
    """
    Detects if any known polyatomic ion appears in `raw`.
    Returns (found, key, comp_dict, charge, name, position) where position is 'prefix'/'suffix' or None
    """
    for key, (comp, charge, name) in charges.POLYATOMIC.items():
        if raw.startswith(key):
            return True, key, comp, charge, name, 'prefix'
        if raw.endswith(key):
            return True, key, comp, charge, name, 'suffix'
        # also check internal occurrences (less common for salts but safe)
        if key in raw:
            return True, key, comp, charge, name, 'internal'
    return False, None, None, None, None, None


'''
def split_cation_anion(compound_raw: str):
    """
    Heuristic split of an ionic formula into (cation_str, anion_str).
    Works for common formulas like: NaCl, CuSO4, NH4Cl, Ca(OH)2 (parentheses handled in parse).
    """
    raw = compound_raw.replace(" ", "")
    # Handle acids (H at start but not H2O)
    if raw.startswith("H") and raw != "H2O":
        # acid -> cation is H (implicit); anion is remainder
        return "H", raw[1:]
    # detect polyatomic ions
    found, key, comp, charge, name, pos = detect_polyatomic_in_formula(raw)
    if found:
        if pos in ('suffix', 'internal'):
            # assume cation is what's before the matched suffix
            prefix = raw[:raw.rfind(key)]
            if prefix == "":  # compound begins with polyatomic? get prefix fallback
                # e.g., "NH4Cl" handled below by prefix detection, but here suffix/location might be internal
                pass
            else:
                return prefix, key
        if pos == 'prefix':
            # polyatomic cation
            suffix = raw[len(key):]
            return key, suffix
    # fallback: try match element symbol as prefix (common for metal salts)
    for sym in ELEMENT_SYMBOLS:
        if raw.startswith(sym):
            rest = raw[len(sym):]
            if rest == "":
                # it's a pure element (not a compound)
                return sym, ""
            return sym, rest
    # last resort: attempt to split in the middle (very fragile)
    mid = len(raw)//2
    return raw[:mid], raw[mid:]
'''

def match_polyatomic(sub_dict):
    """Try to identify sub_dict as n × some polyatomic.
       Returns (ion_symbol, multiplier) or (None, 1)."""
    for ion, (comp, charge, _) in charges.POLYATOMIC.items():
        factor = None
        ok = True
        for el, cnt in comp.items():
            if el not in sub_dict:
                ok = False
                break
            # all ratios must be equal
            ratio = sub_dict[el] // cnt
            if factor is None:
                factor = ratio
            elif factor != ratio:
                ok = False
                break
        if ok and factor and all(sub_dict[e] == comp[e]*factor for e in comp):
            return ion, factor
    return None, 1

def split_cation_anion(compound_raw: str):
    ordered, counts = parse_formula(compound_raw)
    if len(ordered) == 1:
        return ordered[0][0], ""
    cation = ordered[0][0]

    # Build dict for rest (anion part)
    anion_dict = {}
    for sym, cnt in ordered[1:]:
        anion_dict[sym] = anion_dict.get(sym,0)+cnt

    ion, mult = match_polyatomic(anion_dict)
    if ion:
        return cation, ion  # you can also return (ion, mult) if you want multiplier
    # fallback to raw string
    return cation, "".join(f"{sym}{cnt if cnt>1 else ''}" for sym,cnt in ordered[1:])
