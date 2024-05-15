def gauss_elimination(matrix):
    # Check if the matrix is 2x3
    if len(matrix) != 2 or len(matrix[0]) != 3:
        raise ValueError("Input matrix must be 2x3.")

    # Gauss Elimination for 2 by 3 matrices
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

    # Back-substitution
    x = matrix[0][2]
    y = matrix[1][2]

    return x, y

# Example usage
matrix = [[1, 0, -2], 
          [0, 2, -1]]
result = gauss_elimination(matrix)
# print("Solution: x = {}, y = {}".format(result[0], result[1]))
for row in result:
    print(abs(row))
