def check_Stability():
    check_ChargeBalance()
    check_OctetRule()
    check_BondPolarity()
    
    
def check_ChargeBalance():
    return None

def check_OctetRule():
    return None

def check_CommonOxidationState():
    check_Stability()
    check_Reactivity()

def check_Reactivity():
    check_BondPolarity()
    pass

def check_Electronegativity(left, right):
    """Electronegativity difference less than 0.5 - Nonpolar covalent
    \nBetween 0.5 and 1.7 - Polar covalent
    \nGreater than 1.7 - Ionic
    """
    if left[0].is_metal() or right[0].is_metal(): return "ionic"
    result = abs(left[0] - right[0])
    if result < 0.5: return "nonpolar_covalent"
    elif result >= 0.5 or result <=1.7: return "polar_covalent"
    else: return "ionic"

def check_ChemicalNomenclature():
    """NOTHING"""
    return

def check_PhysicalState():
    """NOTHING"""
    return

def check_PhysicalProperties():
    """
    influenced by factors such as molecular structure, 
    intermolecular forces, and chemical composition.
    """
    pass

def check_BondPolarity():
    check_Electronegativity()
