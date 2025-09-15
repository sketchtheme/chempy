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

#needs refinement
def dict_to_formula(counts: dict) -> str:
    """
    Convert element-count dict into a conventional chemical formula.
    - Detects polyatomic groups (SO4, NO3, OH, etc.)
    - Handles acids (H first) and salts (metal first)
    - Falls back to Hill system ordering if unknown
    """
    # First, check if the dict exactly matches a known polyatomic
    for ion, (comp, charge, name) in charges.POLYATOMIC.items():
        if comp == counts:
            return ion

    parts = []

    # Acid convention: if H present and nonmetal anion exists, put H first
    if "H" in counts and len(counts) > 1:
        hcount = counts["H"]
        parts.append("H" + (str(hcount) if hcount > 1 else ""))
        # remove so we don’t reuse
        counts = {el:cnt for el,cnt in counts.items() if el != "H"}

    # Next: if a metal is present, put it first
    metals = [el for el in counts if el in rules.ACTIVITY_SERIES]
    if metals:
        for m in metals:
            c = counts[m]
            parts.append(m + (str(c) if c > 1 else ""))
        counts = {el:cnt for el,cnt in counts.items() if el not in metals}

    # Remaining elements/polyatomics → alphabetical
    for el in sorted(counts.keys()):
        cnt = counts[el]
        parts.append(el + (str(cnt) if cnt > 1 else ""))

    return "".join(parts)

def clean_ion(sym: str) -> str:
    """
    Normalize ion string:
    - Remove outer parentheses and trailing multipliers, e.g. (NO3)2 -> NO3
    - Remove simple trailing digits that represent count, e.g. Cl2 -> Cl
    - Keep digits that are part of polyatomic identity (NO3, SO4, PO4, etc.)
    """
    # (X)2 -> X
    m = re.match(r'^\((.+)\)\d+$', sym)
    if m:
        return m.group(1)
    # If matches known polyatomic exactly, keep it
    if sym in charges.POLYATOMIC:
        return sym
    # Otherwise strip trailing digits (like Cl2 -> Cl)
    return re.sub(r'\d+$', '', sym)

    
def split_cation_anion(compound_raw: str):
    ordered, counts = parse_formula(compound_raw)

    # pure element case
    if len(ordered) == 1:
        return ordered[0][0], ""

    # acid rule: H at start
    if ordered[0][0] == "H" and compound_raw != "H2O":
        return "H", match_polyatomic_or_fallback(ordered[1:])

    # default: first = cation, rest = anion
    cation = ordered[0][0]
    anion = match_polyatomic_or_fallback(ordered[1:])
    return clean_ion(cation), clean_ion(anion)


def match_polyatomic_or_fallback(anion_parts):
    # build dict from the part
    sub_dict = {}
    for sym, cnt in anion_parts:
        sub_dict[sym] = sub_dict.get(sym, 0) + cnt

    # try match known polyatomics
    for ion, (comp, charge, _) in charges.POLYATOMIC.items():
        factor = None
        valid = True
        for el, c in comp.items():
            if el not in sub_dict:
                valid = False
                break
            ratio = sub_dict[el] // c
            if factor is None:
                factor = ratio
            elif factor != ratio:
                valid = False
                break
        if valid and factor and all(sub_dict[e] == comp[e]*factor for e in comp):
            return ion  # return canonical symbol like SO4

    # fallback: rebuild string
    return "".join(f"{sym}{cnt if cnt > 1 else ''}" for sym, cnt in anion_parts)
