import numpy as np
import os
from matrix import Matrix


def main():
    np.random.seed(0)
    data1 = np.random.randint(0, 10, (10, 10)).tolist()
    data2 = np.random.randint(0, 10, (10, 10)).tolist()

    m1 = Matrix(data1)
    m2 = Matrix(data2)

    res_add = m1 + m2
    res_add.save("artifacts/3.1/matrix+.txt")

    res_mul = m1 * m2
    res_mul.save("artifacts/3.1/matrix*.txt")

    res_matmul = m1 @ m2
    res_matmul.save("artifacts/3.1/matrix@.txt")

    print("Artifacts for 3.1 generated.")


if __name__ == "__main__":
    main()
