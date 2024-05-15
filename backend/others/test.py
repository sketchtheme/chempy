import itertools

def check_Stability(molecule):
    # Check if the molecule is stable
    return True

def check_ChargeBalance(molecule):
    # Check if the molecule is charge balanced
    return True

def check_OctetRule(molecule):
    # Check if the atoms in the molecule follow the octet rule
    return all([int(atom["valence"]) == 8 for atom in molecule])

def check_CommonOxidationState(molecule):
    # Check if the oxidation states are common
    oxidation_states = set()
    for atom in molecule:
        oxidation_states.update(atom["oxidation_states"])
    return len(oxidation_states) == 1

def check_Reactivity(molecule):
    reactive_groups = []
    import json
    with open('data.json', 'r') as file:
        get_groups = json.load(file)
        for i in range(1, len(get_groups)):
            if get_groups[i]["group"] == "1":
                reactive_groups.append(get_groups[i]["atomic_symbol"])
        for i in range(len(get_groups)):
            if get_groups[i]["group"] == "2":
                reactive_groups.append(get_groups[i]["atomic_symbol"])
        fount = 0
        for i in range(len(get_groups)):
            if get_groups[i]["group"] == "17":
                fount+=1
                reactive_groups.append(get_groups[i]["atomic_symbol"])
            if fount>3:
                break
    for atom in molecule:
        if atom["atomic_symbol"] in reactive_groups:
            return True
    return False

def check_Electronegativity(left, right):
    # Check the electronegativity difference between elements on the left and right side of the reaction
    left_en = float(left["electronegativity"])
    right_en = float(right["electronegativity"])
    return abs(left_en - right_en) < 1.7

def check_ChemicalNomenclature(molecule):
    # Check the chemical nomenclature of the molecule
    return True

def check_PhysicalState(molecule):
    # Check the physical state of the molecule
    states = set(atom["phase"] for atom in molecule)
    return len(states) == 1

def check_PhysicalProperties(molecule):
    # Check the physical properties of the molecule
    return True

def check_BondPolarity(molecule):
    # Check the bond polarity of the molecule
    return True

def generate_synthesis_reactions(elements):
    reactions = []
    for left, right in itertools.combinations(elements, 2):
        if check_Electronegativity(left, right):
            molecule = [left, right]
            if (check_Stability(molecule) and
                check_ChargeBalance(molecule) and
                check_OctetRule(molecule) and
                check_CommonOxidationState(molecule) and
                check_Reactivity(molecule) and
                check_ChemicalNomenclature(molecule) and
                check_PhysicalState(molecule) and
                check_PhysicalProperties(molecule) and
                check_BondPolarity(molecule)):
                reaction = f"{left['atomic_symbol']} + {right['atomic_symbol']} -> {left['name']} + {right['name']}"
                reactions.append(reaction)
    return reactions

# Example usage:
hydrogen = {
    "atomic_num": "1", 
    "atomic_symbol": "H", 
    "name": "Hydrogen", 
    "origin_of_name": "Greekelementshydro-and-gen, 'water-forming'", 
    "group_of": "1", 
    "period": "1", 
    "block": "s-block", 
    "atomic_mass": "1.0080", 
    "density": "0.00008988", 
    "melt_point": "14.01", 
    "boil_point": "20.28", 
    "heat_capacity": "14.304", 
    "electronegativity": "2.20", 
    "natural_abundance": "1400", 
    "origin": "primordial", 
    "phase": "gas", 
    "oxidation_states": ["1", " 0", " -1"], 
    "valence": "1"
}

oxygen = {
    "atomic_num": "8", 
    "atomic_symbol": "O", 
    "name": "Oxygen", 
    "origin_of_name": "Greekelementsacid-former", 
    "group_of": "16", 
    "period": "2", 
    "block": "p-block", 
    "atomic_mass": "15.999", 
    "density": "0.001429", 
    "melt_point": "54.36", 
    "boil_point": "90.20", 
    "heat_capacity": "5.696", 
    "electronegativity": "3.44", 
    "natural_abundance": "461000", 
    "origin": "primordial", 
    "phase": "gas", 
    "oxidation_states": ["-2", " -1", " 0", " 1"], 
    "valence": "2"
}

elements = [hydrogen, oxygen]

synthesis_reactions = generate_synthesis_reactions(elements)
# for reaction in synthesis_reactions:
#     print(reaction)

for left, right in itertools.combinations(elements, 2):
    if check_Electronegativity(left, right):
        molecule = [left, right]
        print(check_Reactivity(molecule=molecule))
