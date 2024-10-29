from __future__ import annotations
from typing import Any, Optional


class Node:
    def __init__(self, row: int, col: int, value: Any) -> None:
        self.row: int = row
        self.col: int = col
        self.value: Any = value
        self.next_row: Optional[int] = None
        self.next_col: Optional[int] = None


class SparseMatrix:
    def __init__(self, row_number: int, col_number: int) -> None:
        self.row_number: int = row_number
        self.col_number: int = col_number
        self.row_heads: list = [None] * row_number
        self.col_heads: list = [None] * col_number

    def insert(self, row: int, col: int, value: Any) -> None:
        if value == 0:
            return
        new_node = Node(row, col, value)
        if self.row_heads[row] is None or self.row_heads[row].col > col:
            new_node.next_row = self.row_heads[row]
            self.row_heads[row] = new_node
        else:
            current = self.row_heads[row]
            while current.next_row and current.next_row.col < col:
                current = current.next_row
            new_node.next_row = current.next_row
            current.next_row = new_node

        if self.col_heads[col] is None or self.col_heads[col].row > row:
            new_node.next_col = self.col_heads[col]
            self.col_heads[col] = new_node
        else:
            current = self.col_heads[col]
            while current.next_col and current.next_col.row < row:
                current = current.next_col
            new_node.next_col = current.next_col
            current.next_col = new_node

    def multiply_by_scalar(self, scalar: float) -> None:
        for row in range(self.row_number):
            current = self.row_heads[row]
            while current:
                current.value *= scalar
                current = current.next_row

    def transpose(self) -> SparseMatrix:
        transposed = SparseMatrix(self.col_number, self.row_number)
        for row in range(self.row_number):
            current = self.row_heads[row]
            while current:
                transposed.insert(current.col, current.row, current.value)
                current = current.next_row
        return transposed

    def copy(self) -> SparseMatrix:
        copied_matrix = SparseMatrix(self.row_number, self.col_number)
        for row in range(self.row_number):
            current = self.row_heads[row]
            while current:
                copied_matrix.insert(current.row, current.col, current.value)
                current = current.next_row
        return copied_matrix

    def __add__(self, other: SparseMatrix) -> SparseMatrix:
        if self.row_number != other.row_number or self.col_number != other.col_number:
            raise ValueError("Матриці мають бути однакового розміру")

        result = self.copy()
        for row in range(other.row_number):
            current_other = other.row_heads[row]
            while current_other:
                existing_value = result[current_other.row, current_other.col]
                new_value = existing_value + current_other.value
                if new_value != 0:
                    result.insert(current_other.row, current_other.col, new_value)
                current_other = current_other.next_row
        return result

    def __getitem__(self, row_col: tuple[int, int]) -> Any:
        row, col = row_col
        current = self.row_heads[row]
        while current and current.col <= col:
            if current.col == col:
                return current.value
            current = current.next_row
        return 0

    def __str__(self) -> str:
        results = []
        for row in range(self.row_number):
            current = self.row_heads[row]
            row_values = []
            for col in range(self.col_number):
                if current and current.col == col:
                    row_values.append(str(current.value))
                    current = current.next_row
                else:
                    row_values.append("0")
            results.append(" ".join(row_values))
        return "\n".join(results)


if __name__ == '__main__':
    matrix = SparseMatrix(3, 3)
    matrix.insert(0, 0, 1)
    matrix.insert(1, 1, 2)
    matrix.insert(2, 2, 3)
    matrix.insert(0, 2, 5)

    print(f"Початкова матриця:\n{matrix}")
    print("Отримання елементів по індексу:")
    print(matrix[0, 0])
    print(matrix[0, 2])

    matrix.multiply_by_scalar(2)
    print(f"\nМатриця після множення на 2:\n{matrix}")

    transposed = matrix.transpose()
    print(f"\nТранспонована матриця:\n{transposed}")

    print(f"\nДодавання матриць:\n{matrix + transposed}")
