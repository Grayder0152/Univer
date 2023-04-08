class MatrixElement:
    def __init__(self, value: int = 0, next_row_value=None, next_column_value=None):
        self._value = value
        self.next_row_value = next_row_value
        self.next_column_value = next_column_value

    def __repr__(self):
        return str(self._value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value: int):
        if new_value == 0:
            raise ValueError("Value must not equal 0!")
        if not isinstance(new_value, int):
            raise TypeError("Value must be int")
        self._value = new_value


class Matrix:
    def __init__(self, n: int, m: int):
        self.n = n
        self.m = m
        self.matrix: list[list[MatrixElement]] = [[MatrixElement() for _ in range(n)] for _ in range(m)]
        for y in range(m):
            for x in range(n):
                if x != n - 1:
                    self.matrix[y][x].next_row_value = self.matrix[y][x + 1]
                if y != m - 1:
                    self.matrix[y][x].next_column_value = self.matrix[y + 1][x]

    def __getitem__(self, item: list[int, int]):
        if len(item) != 2 or item[0] > self.n - 1 or item[1] > self.m - 1:
            raise ValueError(f"Incorrect coord: {item}")

        return self.matrix[item[0]][item[1]]

    def __setitem__(self, key, value):
        self[key].value = value

    def __repr__(self):
        res = ""
        for row in self.matrix:
            res += f"{row}\n"
        return res

    def __mul__(self, number: int):
        for row in self.matrix:
            element = row[0]
            while element is not None:
                element.value *= number
                element = element.next_row_value

    def __add__(self, other_matrix):
        if not isinstance(other_matrix, Matrix):
            raise TypeError('Other matrix must be Matrix type!')

        if self.n != other_matrix.n or self.m != other_matrix.m:
            raise ValueError('Matrices must be the same size!')
        new_matrix = Matrix(self.n, self.m)

        for i in range(self.m):
            for j in range(self.n):
                v = self[i, j].value + other_matrix[i, j].value
                if v != 0:
                    new_matrix[i, j] = v
        return new_matrix

    def __invert__(self):
        for i in range(self.m):
            for j in range(i, self.n):
                self.matrix[i][j], self.matrix[j][i] = self.matrix[j][i], self.matrix[i][j]

        for row in self.matrix:
            for i in range(self.n):
                element = row[i]
                element.next_row_value, element.next_column_value = element.next_column_value, element.next_row_value


if __name__ == '__main__':
    matrix1 = Matrix(3, 3)
    matrix2 = Matrix(3, 3)
    matrix1[0, 0] = 1
    matrix1[1, 1] = 2
    matrix1[2, 0] = 3
    matrix2[0, 0] = 1
    matrix2[1, 1] = 2
    matrix1[2, 0] = 3

    matrix = matrix1 + matrix2
