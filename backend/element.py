some = {
    "atomic_num": "1", 
    "atomic_symbol": "H", 
    "name": "Hydrogen", 
    "origin_of_name": "Greekelementshydro-and-gen, 'water-forming'", 
    "group": "1", 
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

s = ""
for i in some:
    s+=f"self.{i} = {i}\n"
print(s)
class Element:
    def __init__(self, atomic_num, atomic_symbol, name, origin_of_name, group, period, block, atomic_mass, density, melt_point, boil_point, heat_capacity, electronegativity, natural_abundance, origin, phase, oxidation_states, valence):
        self.atomic_num = atomic_num
        self.atomic_symbol = atomic_symbol
        self.name = name
        self.origin_of_name = origin_of_name
        self.group = group
        self.period = period
        self.block = block
        self.atomic_mass = atomic_mass
        self.density = density
        self.melt_point = melt_point
        self.boil_point = boil_point
        self.heat_capacity = heat_capacity
        self.electronegativity = electronegativity
        self.natural_abundance = natural_abundance
        self.origin = origin
        self.phase = phase
        self.oxidation_states = oxidation_states
        self.valence = valence

    def is_non_metal(self):
        non_metals = ['H', 'He', 'C', 'N', 'O', 'F', 'Ne', 'P', 'S', 'Cl', 'Ar', 'Se', 'Br', 'Kr', 'I', 'Xe', 'At', 'Rn']
        if self.atomic_symbol in non_metals:
            return True
        return False
    def is_metal(self):
        metals = ['Al', 'Ga', 'In', 'Sn', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Uut', 'Uuq', 'Uup', 'Uuh', 'Uus', 'Uuo', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og']
        if self.atomic_symbol in metals:
            return True
        return False
    def is_alkali_metal(self):
        alkali_metals = ['Li', 'Na', 'K', 'Rb', 'Cs', 'Fr']
        if self.atomic_symbol in alkali_metals:
            return True
        return False
    def is_alkali_earth_metal(self):
        alkaline_earth_metals = ['Be', 'Mg', 'Ca', 'Sr', 'Ba', 'Ra']
        if self.atomic_symbol in alkaline_earth_metals:
            return True
        return False
    def is_transition_metal(self):
        transition_metals = ['Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og']
        if self.atomic_symbol in transition_metals:
            return True
        return False  
    def is_metalloid(self):        
        metalloids = ['B', 'Si', 'Ge', 'As', 'Sb', 'Te', 'Po', 'At']
        if self.atomic_symbol in metalloids:
            return True
        return False
    def is_halogen(self):        
        halogens = ['F', 'Cl', 'Br', 'I', 'At']
        if self.atomic_symbol in halogens:
            return True
        return False
    def is_noble_gas(self):
        noble_gases = ['He', 'Ne', 'Ar', 'Kr', 'Xe', 'Rn']
        if self.atomic_symbol in noble_gases:
            return True
        return False
    def is_lanthanide(self):
        lanthanides = ['La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu']
        if self.atomic_symbol in lanthanides:
            return True
        return False
    def is_actinide(self):
        actinides = ['Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr']
        if self.atomic_symbol in actinides:
            return True
        return False
