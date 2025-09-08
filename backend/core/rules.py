#--- ruleset ---

SOLUBLE_SERIES = [
    #SO4^2
    'Li', 'Na', 'K', 'Rb', 'Cs', 'NH4', 
    'NO3', 'C2H3O2', 'Cl', 'Br', 'I', 'SO4'
]
SOLUBLE_EXCEPTION_SERIES = [
    'AgCl', 'AgBr', 'AgI', 'Hg2Cl', 'Hg2Br', 'Hg2I', 'Pb2Cl', 
    'Pb2Br', 'Pb2I', 'Hg2SO4', 'Pb2SO4', 'Sr2SO4', 'Ba2SO4'
]
INSOLUBLE_SERIES = [
    'CO3', 'PO4', 'OH'
]
INSOLUBLE_EXCEPTION_SERIES = [
    'Li2CO3', 'Li3PO4', 'Na2CO3', 'Na3PO4', 'K2CO3', 'K3PO4', 'Rb2CO3', 
    'Rb3PO4', 'Cs2CO3', 'Cs3PO4', '(NH4)2CO3', '(NH4)3PO4', 'LiOH', 
    'NaOH', 'KOH', 'RbOH', 'CsOH', 'NH4OH', 'Sr(OH)2', 'Ba(OH)2'
]
ACTIVITY_SERIES = [
    'Li', 'K', 'Ba', 'Sr', 'Ca', 'Na', 'Mg', 'Al', 
    'Mn', 'Zn', 'Cr', 'Fe', 'Ni', 'Sn', 'Pb', 
    'H2', 'Cu', 'Hg', 'Ag', 'Pd', 'Pt', 'Au'
]
HALOGEN_ORDER = [
    # not in the most reactive order
    'H', 'F', 'Cl', 'Br', 'I', 'At'
]
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
