import numpy as np
import os
from matrix_numpy import Matrix


def main():
    np.random.seed(0)
    data1 = np.random.randint(0, 10, (10, 10))
    data2 = np.random.randint(0, 10, (10, 10))

    m1 = Matrix(data1)
    m2 = Matrix(data2)

    res_add = m1 + m2
    res_add.save("artifacts/3.2/matrix+.txt")

    res_mul = m1 * m2
    res_mul.save("artifacts/3.2/matrix*.txt")

    res_matmul = m1 @ m2
    res_matmul.save("artifacts/3.2/matrix@.txt")

    print("Artifacts for 3.2 generated.")


if __name__ == "__main__":
    main()
