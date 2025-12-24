import numpy as np


class HashMixin:
    def __hash__(self):
        """
        Хэш-функция: сумма элементов матрицы по модулю 51 (для искусственного создания коллизий).
        """
        res = 0
        for row in self.data:
            for val in row:
                res += val
        return int(res % 51)


class Matrix(HashMixin):
    _matmul_cache = {}

    def __init__(self, data):
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0]) if self.rows > 0 else 0

    def __add__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Dimensions must match for addition")
        
        result = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(self.data[i][j] + other.data[i][j])
            result.append(row)
        return Matrix(result)

    def __mul__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Dimensions must match for element-wise multiplication")
        
        result = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(self.data[i][j] * other.data[i][j])
            result.append(row)
        return Matrix(result)

    def __matmul__(self, other):
    
        key = (hash(self), hash(other))
        if key in self._matmul_cache:
            return self._matmul_cache[key]

        if self.cols != other.rows:
            raise ValueError("Dimensions must match for matrix multiplication")

        result = []
        for i in range(self.rows):
            row = []
            for j in range(other.cols):
                val = sum(self.data[i][k] * other.data[k][j] for k in range(self.cols))
                row.append(val)
            result.append(row)

        res_matrix = Matrix(result)
        self._matmul_cache[key] = res_matrix
        return res_matrix

    def __str__(self):
        return "\n".join(["\t".join(map(str, row)) for row in self.data])

    def save(self, filepath):
        with open(filepath, "w") as f:
            f.write(str(self))

    def __eq__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            return False
        return self.data == other.data

    # Explicitly use hash from mixin because __eq__ sets __hash__ to None
    __hash__ = HashMixin.__hash__
