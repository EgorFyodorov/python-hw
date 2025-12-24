import numpy as np
from matrix_hash import Matrix


def main():
    # Ищем коллизию вручную, зная хэш-функцию (сумма % 73)

    # A: [[1, 0], [0, 0]] -> sum=1, hash=1
    A_data = [[1, 0], [0, 0]]
    A = Matrix(A_data)

    # C: [[0, 1], [0, 0]] -> sum=1, hash=1
    # A != C
    C_data = [[0, 1], [0, 0]]
    C = Matrix(C_data)

    # B = D: Identity [[1, 0], [0, 1]] -> sum=2, hash=2
    B_data = [[1, 0], [0, 1]]
    B = Matrix(B_data)
    D = Matrix(B_data)  # D is a new object, same content as B

    # Проверки условий задачи
    assert hash(A) == hash(C), f"Hashes should match: {hash(A)} vs {hash(C)}"
    assert A != C, "A should not equal C"
    assert B == D, "B should equal D"

    # Настоящее произведение A @ B
    AB = A @ B  # Это запишется в кэш

    # Произведение C @ D
    # Из-за кэша вернется результат A @ B, так как hash(A)==hash(C) и hash(B)==hash(D)
    CD_cached = C @ D

    # Настоящий результат C @ D (вычислим вручную или очистив кэш, но нам нужно сохранить его в файл)
    # Для получения настоящего результата создадим C_clean, D_clean без кэша (или просто зная математику)
    # Но проще всего создать новые объекты Matrix и отключить кэш или просто посчитать руками для сохранения.
    # В задаче просят "CD.txt - настоящий результат".
    # Можем просто посчитать:
    C_real_mul_D_data = [[0, 1], [0, 0]]  # так как B - identity
    C_real_mul_D = Matrix(C_real_mul_D_data)

    # Проверка, что кэш сработал некорректно (для себя)
    # assert AB.data == CD_cached.data # Они должны быть равны из-за коллизии
    # assert CD_cached.data != C_real_mul_D.data # А результат неверен

    # Сохранение артефактов
    A.save("artifacts/3.3/A.txt")
    B.save("artifacts/3.3/B.txt")
    C.save("artifacts/3.3/C.txt")
    D.save("artifacts/3.3/D.txt")
    AB.save("artifacts/3.3/AB.txt")
    C_real_mul_D.save("artifacts/3.3/CD.txt")

    with open("artifacts/3.3/hash.txt", "w") as f:
        f.write(str(hash(A)))  # Хэш одинаковый для A и C

    print("Artifacts for 3.3 generated.")


if __name__ == "__main__":
    main()
