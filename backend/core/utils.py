#--- helper ---
from backend.core import charges
from math import gcd

def gcd_list(nums):
    return reduce(gcd, [abs(int(n)) for n in nums if n != 0], 0) or 1

#composition
def formula_from_ions(cation: str, c_charge: int, anion: str, a_charge: int):
    """
    Build neutral formula string for cation+anion using cross-over method.
    Handles polyatomic anions (wraps in parentheses when count>1).
    """
    # normalize charges positive for cation, negative for anion
    c = abs(int(c_charge))
    a = abs(int(a_charge))

    g = gcd(c, a)
    sub_c = a // g  # number of cation units
    sub_a = c // g  # number of anion units

    def fmt_part(sym, count, is_poly):
        if count == 1:
            return sym
        return f"({sym}){count}" if is_poly else f"{sym}{count}"
        
    # decide whether anion symbol corresponds to a polyatomic (presence in POLYATOMIC keys)
    is_cation_poly = cation in charges.POLYATOMIC
    is_anion_poly = anion in charges.POLYATOMIC

    c_part = fmt_part(cation, sub_c, is_cation_poly)
    a_part = fmt_part(anion, sub_a, is_anion_poly)
    # Standard convention: cation first
    return c_part + a_part
