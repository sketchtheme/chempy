"""
    Splitting the Reaction:
        You'll need to split the chemical reaction into reactants and products.
        Typically, chemical reactions are represented as strings, so you can start by parsing the reaction string.
        For example, if you have the reaction "H2 + O2 -> H2O," you'll want to split it into reactants ("H2 + O2") and products ("H2O").

    Parsing Reactants and Products:
        After splitting the reaction, you can further parse the reactants and products to identify the chemical species involved.
        You can split each side of the reaction by the '+' symbol to get individual species.
        Then, for each species, you can parse the coefficients and chemical formulas.

    Building the Matrix:
        With the information about the chemical species and their coefficients, you can construct the matrix for the Gaussian elimination.
        Each row of the matrix represents a chemical species, and each column represents an element.
        Populate the matrix based on the coefficients of elements in each species.

    Balancing the Reaction:
        Use the gaussian_elimination function to balance the reaction represented by the matrix.
        The result of the Gaussian elimination will provide the coefficients for balancing the reaction.

    Constructing the Balanced Reaction:
        After obtaining the coefficients, you can construct the balanced chemical reaction.
"""
import re

def balance_reaction(reaction):
    # Split the reaction into reactants and products
    reactants, products = reaction.split('->')

    # Parse reactants and products
    reactant_species = [s.strip() for s in reactants.split('+')]
    product_species = [s.strip() for s in products.split('+')]

    # Create a set of all unique elements in the reaction
    all_elements = set()
    for species in reactant_species + product_species:
        elements = re.findall(r'([A-Z][a-z]*)(\d*)', species)
        for element, _ in elements:
            all_elements.add(element)

    # Initialize the matrix with zeros
    matrix = [[0 for _ in range(len(all_elements))] for _ in range(len(reactant_species))]

    # Populate the matrix with coefficients based on the elements in each species
    for i, species in enumerate(reactant_species):
        elements = re.findall(r'([A-Z][a-z]*)(\d*)', species)
        for element, coefficient in elements:
            col_index = list(all_elements).index(element)
            matrix[i][col_index] = -int(coefficient) if coefficient else -1

    for i, species in enumerate(product_species):
        elements = re.findall(r'([A-Z][a-z]*)(\d*)', species)
        for element, coefficient in elements:
            col_index = list(all_elements).index(element)
            matrix[i][col_index] = int(coefficient) if coefficient else 1

    # Use Gaussian elimination to balance the reaction
    balanced_matrix = gaussian_elimination(matrix)

    # Construct the balanced reaction
    balanced_reaction = ''
    for i, species in enumerate(reactant_species + product_species):
        coefficient = balanced_matrix[i][-1]
        if coefficient != 0:
            if coefficient > 0:
                balanced_reaction += ' + ' if balanced_reaction else ''
                balanced_reaction += str(coefficient) + ' ' + species
            else:
                balanced_reaction += ' - ' + str(-coefficient) + ' ' + species

    return balanced_reaction

# Example usage:
reaction = "H2 + O2 -> H2O"
balanced = balance_reaction(reaction)
print(balanced)
