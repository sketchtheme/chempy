import re
from sympy import symbols

#------------------------------------------------------------------------REACTION PARSER (all)


def parseReaction(reaction: str):
    """The function to parse chemical reaction.
    
    e.g.
        
        "HCl + O2 -> H2O + Cl"

    Output:
        
        ([{'H': 1, 'Cl': 1}, {'O': 2}], [{'H': 2, 'O': 1}, {'Cl': 1}])

    """
    # making unique list
    unique = []
    elements = re.findall(r"([A-Z][a-z]*)", reaction)
    unique = list(dict.fromkeys(elements).keys())

    reaction = reaction.replace(' ', '').split('->')
    reactant, product = reaction
    reactant = reactant.split('+')
    product = product.split('+')
    # unique = set()

    reactants_list = []
    products_list = []

    # Processing the reactants
    for side in reactant:
        re_side = {}
        elements = re.findall(r"([A-Z][a-z]*)(\d*)", side)
        for element, sub in elements:
            if sub.isdigit():
                sub_count = int(sub)
            else:
                sub_count = 1
            re_side[element] = sub_count
        reactants_list.append(re_side)

    # Processing the products
    for side in product:
        re_side = {}
        elements = re.findall(r"([A-Z][a-z]*)(\d*)", side)
        for element, sub in elements:
            if sub.isdigit():
                sub_count = 0 - int(sub)
            else:
                sub_count = -1
            re_side[element] = sub_count
        products_list.append(re_side)

    return reactants_list, products_list, unique


#------------------------------------------------------------------------GAUSS JORDAN ELIMINATION (2x3, 3x4)


def gaussianElimination(matrix: list):
    """Gauss Jordan Elimination, to reduce matrix into Row Echelon Form
    The logic behind balancing Reactions 
    
    e.g.

        Three By Four:
            [2, 0, -1, 0],
            
            [1, 0, 0, -2],
            
            [0, 1, -1, 0]

        Two By Three:
            [[1, 0, -2], 
            
            [0, 2, -1]]

    """
    if (len(matrix) == 3) and (len(matrix[0]) == 4):
        """
        Reducing 3 by 4 Matrices into Row Echelon Form
        This part is used to balance Reactions that involve Three or More Base Elements, e.g. Single Replacement Reaction
        """
        for col in range(3):
            # Partial Pivoting
            max_row = col
            for i in range(col + 1, 3):
                if abs(matrix[i][col]) > abs(matrix[max_row][col]):
                    max_row = i
            # Swapping the current row with the row containing the maximum value
            matrix[col], matrix[max_row] = matrix[max_row], matrix[col]

            # Making the diagonal element 1
            pivot = matrix[col][col]
            for j in range(4):
                if pivot == 0:
                    continue
                matrix[col][j] /= pivot

            # Eliminating non-zero values below the pivot
            for i in range(col + 1, 3):
                factor = matrix[i][col]
                for j in range(4):
                    matrix[i][j] -= factor * matrix[col][j]

        # Back substitution
        for col in range(2, -1, -1):
            for i in range(col - 1, -1, -1):
                factor = matrix[i][col]
                for j in range(4):
                    matrix[i][j] -= factor * matrix[col][j]
        
        return matrix

    if (len(matrix) == 2) or (len(matrix[0]) == 3):
        """
        Reducing 2 by 3 Matrices into Row Echelon Form
        This part is used to balance Reactions that involve only Two Base Elements, e.g. Synthesis Reaction
        """
        for i in range(2):
            # Normalizing the current row
            pivot = matrix[i][i]
            for j in range(3):
                matrix[i][j] /= pivot

            # Eliminating elements below the pivot
            for k in range(i + 1, 2):
                factor = matrix[k][i]
                for j in range(3):
                    matrix[k][j] -= factor * matrix[i][j]

        return matrix


#------------------------------------------------------------------------SET VECTORS AND BALANCE THE EQUATION (2x3, 3X4)


def setVector(reaction: str):
    reactants_list, products_list, unique = parseReaction(reaction)
    vectors = reactants_list + products_list

    element_variables = []
    for i in range(1, len(vectors) + 1):
        element_variables.append(symbols(f'x_{i}'))

    # Initializing lists for each variable
    lists_of_variables = {key: [] for key in unique}

    # Iterating through vectors and append values to the corresponding lists
    for key in unique:
        for vector in vectors:
            if key in vector:
                lists_of_variables[key].append(vector[key])
            else:
                lists_of_variables[key].append(0)

    # Creating a matrix for Gaussian elimination
    matrix = []
    for i, key in enumerate(unique):
        matrix.append(lists_of_variables[key])
    result = gaussianElimination(matrix)

    # Returning absolute values
    coefficients = []
    for i in result:
        coefficients.append(abs(i[-1]))
    return coefficients


#------------------------------------------------------------------------SUMMARIZE THE COEFFICIENTS (2x3, 3x4) (only in the right order)


def summarize(coefficients: list):
    """Summarizing the result, into appropriate form
    
    e.g. coefficients: [2.0, 0.5] -> [[4, 1], [2]]  |  2 is a factor

    """  
    factor = 1.0

    if len(coefficients) == 2:
        new_values = []

        while True:
            new_coef = []
            for el in coefficients:
                result = factor * el
                new_coef.append(result)

            a1 = str(new_coef[0]).split('.')
            a2 = str(new_coef[1]).split('.')

            if (int(a1[1]) == 0) and (int(a2[1]) == 0):
                new_values.append(new_coef)
                new_values.append([factor])
                break
            factor += 1.0

        correct_values = [[int(x) for x in sublist] for sublist in new_values]
        return correct_values
    
    if len(coefficients) == 3:
        new_values = []

        while True:
            new_coef = []
            for el in coefficients:
                result = factor * el
                new_coef.append(result)

            a1 = str(new_coef[0]).split('.')
            a2 = str(new_coef[1]).split('.')
            a3 = str(new_coef[2]).split('.')

            if (int(a1[1]) == 0):
                if (int(a2[1]) == 0):
                    if (int(a3[1]) == 0):
                        new_values.append(new_coef[:2])
                        new_values.append([new_coef[2],factor])
                        break
            factor += 1.0
        
        correct_values = [[int(x) for x in sublist] for sublist in new_values]
        return correct_values
        
    return


#------------------------------------------------------------------------JOIN THE REACTION WITH IT'S CORRESPONDING COEFFICIENTS


def joinReaction(reaction, coefficients):
    reactants_list, products_list, unique = parseReaction(reaction)  
    coef = summarize(coefficients)
    lefts = []
    rights = []
    all_rights = []
    
    # Joining Synthesis reaction
    if len(coef[1]) == 1:
        for i, el in enumerate(reactants_list):
            for key, value in el.items():
                lefts.append(f"{coef[0][i]}{key}{value}")    

        for i, el in enumerate(products_list):
            for key, value in el.items():
                rights.append(f"{key}{abs(value)}")
            all_rights.append(f"{coef[1][0]}{rights[0]}{rights[1]}")
        
        result = f"{lefts[0]} + {lefts[1]} -> {all_rights[0]}"
        return result
    
    # Joining Single-replacement reaction | "not working" | working
    if len(coef[1]) == 2:
        l = list()
        pl = list()

        # the first reactant
        for key, value in reactants_list[0].items():
            l.append(f'{key}{value}')
        # this probably not single replacement reaction
        if len(l) == 3:
            reactants = f"{coef[0][0]}{l[0]}{l[1]}{l[2]}"
        else:
            reactants = f"{coef[0][0]}{l[0]}{l[1]}"
        lefts.append(reactants)
        
        # the second reactant
        for key, value in reactants_list[1].items():
            lefts.append(f"{coef[0][1]}{key}{value}")

        # the first product
        for key, value in products_list[0].items():
            pl.append(f'{key}{abs(value)}')
        if len(pl) == 3:
            products = f"{coef[1][0]}{pl[0]}{pl[1]}{pl[2]}"
        else:
            products = f"{coef[1][0]}{pl[0]}{pl[1]}"
        rights.append(products)


        # the second product
        pl.clear()
        for key, value in products_list[1].items():
            pl.append(f'{key}{abs(value)}')
        if len(pl) == 3:
            products = f"{coef[1][1]}{pl[0]}{pl[1]}{pl[2]}"
        elif len(pl) == 2:
            products = f"{coef[1][1]}{pl[0]}{pl[1]}"
        else:
            products = f"{coef[1][1]}{pl[0]}"
        rights.append(products)

        result = f"{lefts[0]} + {lefts[1]} -> {rights[0]} + {rights[1]}"
        return result
    
    if len(coef[1] == 3):
        pass

    return


#------------------------------------------------------------------------FINAL


# Example usage:
reaction = "H2O + K -> K2O + H"
# reaction = "Fe + Cl -> FeCl3"
# reaction = "C6H12O6 + O2 -> CO2 + H2O1"

balanced_coefficients = setVector(reaction)
print(joinReaction(reaction, balanced_coefficients))
