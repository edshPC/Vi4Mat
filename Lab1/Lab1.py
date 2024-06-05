import numpy as np

from Vi4Mat.Reader import Reader


class GaussZeidelMatrix(np.ndarray):
    def __new__(cls, dim, array, accuracy):
        instance = np.ndarray.__new__(cls, (dim, dim + 1), buffer=array)
        instance.dim = dim
        instance.accuracy = accuracy
        return instance

    def norma(self):
        C = np.array([
            [-self[i, j] / self[i, i] if i != j else 0 for j in range(self.dim)]
            for i in range(self.dim)
        ])
        # print("C:")
        # print(C)
        norma = max(
            sum(abs(C[:, i]))
            for i in range(self.dim)
        )
        return norma

    def has_diagonal(self):
        for i in range(self.dim):
            row_sum = sum(abs(self[i, :self.dim])) - abs(self[i, i])
            if abs(self[i, i]) < row_sum:
                return False
        return True

    def make_diagonal(self):
        if self.has_diagonal(): return True
        initial = self.copy()
        for i in range(self.dim):
            for j in range(self.dim):
                # Переставляем строки
                self[[i, j]] = self[[j, i]]
                if self.has_diagonal():
                    return True

                # Переставляем столбцы
                self[:, [i, j]] = self[:, [j, i]]
                if self.has_diagonal():
                    return True
        self[:] = initial
        return False

    def approximate(self):
        max_iters = 1000
        # Изначальные матрицы
        A = self[:, :-1]
        B = self[:, -1]
        # Матрицы эквивалентной СЛАУ
        # C = np.array([  # Не используется
        #     [-A[i, j] / A[i, i] if i != j else 0 for j in range(self.dim)]
        #     for i in range(self.dim)
        # ])
        D = np.array([
            B[i] / A[i, i] for i in range(self.dim)
        ])
        # Начальное приближение
        X = D.copy()
        # X = [100] * self.dim

        k = 1
        self.deviations = np.array([0.0] * self.dim)
        while True:
            delta = 0.0
            for i in range(self.dim):
                s = sum(A[i, j] * X[j] for j in range(self.dim) if i != j)
                x = (B[i] - s) / A[i, i]
                d = abs(x - X[i])
                delta = max(d, delta)
                self.deviations[i] = d
                X[i] = x
            if k >= max_iters:
                print("Итерации расходятся!")
                break
            k += 1
            if delta < self.accuracy:
                break
        self.solution = X
        return k


reader = Reader()

dim = reader.readnumber("Введите размерность матрицы: ")
print(f'Введите матрицу {dim}x{dim + 1}')

array = np.array([
    [float(x) for x in reader.readline().split()]
    for i in range(dim)
])
if array.shape[1] != dim + 1:
    print("Некорректный размер матрицы")
    exit()

accuracy = reader.readnumber("Введите точность: ", float)
print()

matrix = GaussZeidelMatrix(dim, array, accuracy)

if matrix.make_diagonal():
    print("Диагональное преобладание матрицы достигнуто")
else:
    print("Диагональное преобладание матрицы невозможно")
print(matrix)

print("Норма по столбцам:", matrix.norma())

iters = matrix.approximate()
print("Приближенное решение матрицы:")
print("X =", matrix.solution)
print("Количество итераций:", iters)
print("Вектор погрешностей:")
print(matrix.deviations)
