# from sympy import symbols

# reaction = "H2O + Cl -> HCl + O2"
# reactants_list = [{'H': 2, 'O': 1}, {'Cl': 1}]
# products_list = [{'H': 1, 'Cl': 1}, {'O': 2}]
# vectors = reactants_list + products_list
# # print(vectors)
# # print()
# unique = {'H', 'O', 'Cl'}

# element_variables = []
# for i in range(1, len(vectors)+1):
#     element_variables.append(symbols(f'x_{i}'))
# # print(element_variables)
# equations = []  # List to store conservation equations


# for i in vectors:
#     print(i)
#     for j in element_variables:
#         j = list()
#         for k in i:
#             if k in unique:
#                 j.append(1)
#                 print(j)
#             else:
#                 j.append(0)
#                 print(j)
             
# ========================

# lists_of_variables = [[] for _ in element_variables]
# # for i, var in enumerate(element_variables):
# #     lists_of_variables[i].append(var)

# for i in vectors:
#     print(i)
#     for k in lists_of_variables:
#         for j in i:
#             if j in unique:
#                 k.append(i[j])
#             else:
#                 k.append(0)

# for i in lists_of_variables:
#     print(i)

# ========================


# **********************************
# **********************************

# # Define your list of dictionaries (vectors)
# vectors = [
#     {'x': 1, 'y': 2, 'z': 3},
#     {'x': 4, 'w': 5},
#     {'y': 6, 'z': 7},
#     {'w': 8},
# ]

# # Create a set of unique keys
# unique = {'x', 'y', 'z'}

# # Initialize lists for each variable
# lists_of_variables = {key: [] for key in unique}

# # Iterate through vectors and append values to the corresponding lists
# for vector in vectors:
#     for key in unique:
#         if key in vector:
#             lists_of_variables[key].append(vector[key])
#         else:
#             lists_of_variables[key].append(0)

# # Append 0 for the missing variable (w in this case)
# for key in vectors[0].keys():
#     if key not in unique:
#         lists_of_variables[key].append(0)

# # Print the result
# for key, values in lists_of_variables.items():
#     print(f'{key}: {values}')


# **********************************
# **********************************



#  CODE THAT WORKS!!!


from sympy import symbols
import re

reaction = "H2O + Cl -> HCl + O2"
reactants_list = [{'H': 2, 'O': 1}, {'Cl': 1}]
products_list = [{'H': -1, 'Cl': -1}, {'O': -2}]
vectors = reactants_list + products_list

# ==================MAKE UNIQUE LIST
unique = []
elements = re.findall(r"([A-Z][a-z]*)", reaction)
unique = list(dict.fromkeys(elements).keys())
print(unique)
# ==================

element_variables = []
for i in range(1, len(vectors) + 1):
    element_variables.append(symbols(f'x_{i}'))

# Initialize lists for each variable
lists_of_variables = {key: [] for key in unique}

# Iterate through vectors and append values to the corresponding lists
for key in unique:
    for vector in vectors:
        if key in vector:
            lists_of_variables[key].append(vector[key])
        else:
            lists_of_variables[key].append(0)

matrix = []
# Print the result
for i, key in enumerate(unique):
    print(f'for the {key} variable in lists_of_variables')
    print(lists_of_variables[key])
    matrix.append(lists_of_variables[key])
print(matrix)





# for j in vectors:
#     print(f'element: {j}')
# for i in element_variables:
#     print(i)



# for element in unique:
#     reactant_coefficient_sum = sum(reactant.get(element, 0) for reactant in reactants_list)
#     product_coefficient_sum = sum(product.get(element, 0) for product in products_list)

#     print(f"{element_variables[element]}* {reactant_coefficient_sum} - {product_coefficient_sum}")
    
#     equation = element_variables[element] * reactant_coefficient_sum - product_coefficient_sum
#     equations.append(equation)

# Solving the system of equations using Gaussian elimination


# coefficients = {element: 0 for element in unique}
# print(coefficients)


#  CODE THAT DOESN'T WORK

def balanceReaction(reaction):
    reactants_list, products_list, unique = parseReaction(reaction)
    print(reactants_list, products_list, unique)

    # Initializing variables for each unique element
    element_variables = {element: symbols(f'x_{element}') for element in unique}

    # Setting up equations for conservation of each element
    equations = []  # List to store conservation equations

    for element in unique:
        reactant_coefficient_sum = sum(reactant.get(element, 0) for reactant in reactants_list)
        product_coefficient_sum = sum(product.get(element, 0) for product in products_list)

        print(f"{element_variables[element]}* {reactant_coefficient_sum} - {product_coefficient_sum}")
        
        equation = element_variables[element] * reactant_coefficient_sum - product_coefficient_sum
        equations.append(equation)

    # Solving the system of equations using Gaussian elimination
    coefficients = {element: 0 for element in unique}

    print(equations)
    print()
    # Creating a matrix for Gaussian elimination
    matrix = []
    for equation in equations:
        row = [equation.coeff(element_variables[element]) if element in equation.free_symbols else 0 for element in unique]
        row.append(-equation)
        
        print(row)
        
        matrix.append(row)
    
    print()
    print(matrix)
    print()

    result = gaussianElimination(matrix)
    
    print(result)
    print()
    
    for i, element in enumerate(unique):
        coefficients[element] = result[i][3]

    return coefficients





# working!!!
# from sympy import symbols, Eq, solve

# def balance_reaction(reaction):
#     # Step 1: Parse the reaction
#     reactants_list, products_list, unique = parseReaction(reaction)

#     # Step 2: Initialize variables for each unique element
#     element_variables = {element: symbols(f'x_{element}') for element in unique}

#     # Step 3: Set up equations for conservation of each element
#     equations = []  # List to store conservation equations

#     for element in unique:
#         reactant_coefficient_sum = sum(reactant.get(element, 0) for reactant in reactants_list)
#         product_coefficient_sum = sum(product.get(element, 0) for product in products_list)

#         equation = Eq(element_variables[element] * reactant_coefficient_sum, product_coefficient_sum)
#         equations.append(equation)

#     # Step 4: Solve the system of equations
#     solution = solve(equations)

#     # Step 5: Extract the balanced coefficients from the solution
#     balanced_coefficients = {str(element): float(solution[element_variables[element]]) for element in unique}

#     return balanced_coefficients
