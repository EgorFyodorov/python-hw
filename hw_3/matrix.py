class Matrix:
    def __init__(self, data):
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0]) if self.rows > 0 else 0

    def __add__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError(
                f"Shape mismatch for addition: ({self.rows}, {self.cols}) vs "
                f"({other.rows}, {other.cols})"
            )

        result = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(self.data[i][j] + other.data[i][j])
            result.append(row)
        return Matrix(result)

    def __mul__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError(
                f"Shape mismatch for element-wise multiplication: "
                f"({self.rows}, {self.cols}) vs ({other.rows}, {other.cols})"
            )

        result = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(self.data[i][j] * other.data[i][j])
            result.append(row)
        return Matrix(result)

    def __matmul__(self, other):
        if self.cols != other.rows:
            raise ValueError(
                f"Shape mismatch for matrix multiplication: "
                f"({self.rows}, {self.cols}) vs ({other.rows}, {other.cols})"
            )

        result = []
        for i in range(self.rows):
            row = []
            for j in range(other.cols):
                val = sum(self.data[i][k] * other.data[k][j] for k in range(self.cols))
                row.append(val)
            result.append(row)
        return Matrix(result)

    def __str__(self):
        return "\n".join(["\t".join(map(str, row)) for row in self.data])

    def save(self, filepath):
        with open(filepath, "w") as f:
            f.write(str(self))
