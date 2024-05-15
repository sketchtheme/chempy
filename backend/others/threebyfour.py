def gaussian_elimination(matrix):
    # Ensure the matrix is 3x4
    if len(matrix) != 3 or len(matrix[0]) != 4:
        raise ValueError("Matrix must be 3x4")

    # Perform Gaussian Elimination
    for col in range(3):
        # Partial pivoting: Find the row with the maximum absolute value in the current column
        max_row = col
        for i in range(col + 1, 3):
            if abs(matrix[i][col]) > abs(matrix[max_row][col]):
                max_row = i

        # Swap the current row with the row containing the maximum value
        matrix[col], matrix[max_row] = matrix[max_row], matrix[col]

        # Make the diagonal element 1
        pivot = matrix[col][col]
        for j in range(4):
            matrix[col][j] /= pivot

        # Eliminate non-zero values below the pivot
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

# Example usage
matrix = [
    [2, 0, -1, 0],
    [1, 0, 0, -2],
    [0, 1, -1, 0]
]

result = gaussian_elimination(matrix)

# Print the result
for row in result:
    print(row)
