def input_matrix():
    print("Input order of matrix")
    size = int(input("Choose matrix size (rows and columns): "))
    print(f"Matrix A: {size}x{size}\n" + "-" * 20)
    
    matrix = []
    print("Input elements of matrix")
    for i in range(size):
        row = [int(input(f"A {i + 1}, {j + 1}: ")) for j in range(size)]
        matrix.append(row)
    
    print("-" * 20)
    return matrix


def inverse_matrix(matrix):
    determinant = find_determinant(matrix)
    if determinant == 0:
        print("Matrix is Singular! (Determinant = 0)")
        return None
    size = len(matrix)
    minors = [[find_determinant([[matrix[x][y] for y in range(size) if y != j] 
                                  for x in range(size) if x != i]) 
               for j in range(size)] 
              for i in range(size)]
    
    cofactors = [[(-1) ** (i + j) * minors[i][j] for j in range(size)] for i in range(size)]
    adjugate = [[cofactors[j][i] for j in range(size)] for i in range(size)]
    inverse = [[adjugate[i][j] / determinant for j in range(size)] for i in range(size)]
    
    return inverse


def find_determinant(matrix):
    size = len(matrix)
    if size == 1:
        return matrix[0][0]
    elif size == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    
    determinant = sum(matrix[0][i] * find_determinant([[matrix[x][y] for y in range(size) if y != i] 
                                                       for x in range(1, size)]) * (-1) ** i 
                      for i in range(size))
    return determinant


def print_matrix(matrix, text=""):
    if matrix is None:
        return
    
    print(f"{text}")
    for row in matrix:
        print("\t[", " ".join(f"{round(num, 3)}" for num in row), "]")
    print()


def main():
    print("Calculator: inverse matrix")
    while True:
        matrix = input_matrix()
        inverse = inverse_matrix(matrix)
        
        print("Calculation results")
        print_matrix(matrix, "A:")
        print_matrix(inverse, "A^-1:")
        print("-" * 20)
        
        if input("Would you like to make another calculation? (y/n): ").lower() != "y":
            print("Got it")
            break


if __name__ == "__main__":
    main()