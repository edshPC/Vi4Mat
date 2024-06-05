import numpy as np
import sympy as sp


class Function:
    valid = True
    function = None
    lmb = None

    def polinome_coef(self, X, Y, k):
        # Создает матрицу k+1xk+1, где элемент Aij высчитывается как sum_k(xk^(i+j))
        M = np.fromfunction(
            np.vectorize(lambda i, j: np.sum(X ** (i + j))),
            (k + 1, k + 1), dtype=float)
        B = np.fromfunction(
            np.vectorize(lambda i: np.sum(X ** i * Y)),
            (k + 1,), dtype=float)

        print(M)
        print(B)
        try:
            A = np.linalg.solve(M, B)
        except:
            return np.zeros(k + 1)
        return A

    def function_from_coef(self, A):
        x = sp.symbols('x')
        F = sum(A[i] * x ** i for i in range(len(A)))
        return F

    def make_function(self, X, Y):
        pass

    def make_lambda(self, X, Y):
        self.make_function(X, Y)
        self.lmb = sp.lambdify(sp.symbols('x'), self.function)
        if not self.function.free_symbols:
            self.valid = False
            print(self, "функция невозможна")

    def __call__(self, *args):
        return self.lmb(*args)


class Linear(Function):
    def make_function(self, X, Y):
        A = self.polinome_coef(X, Y, 1)
        self.function = self.function_from_coef(A)

    def __str__(self):
        return 'Линейная'


class Quadratic(Function):
    def make_function(self, X, Y):
        A = self.polinome_coef(X, Y, 2)
        self.function = self.function_from_coef(A)

    def __str__(self):
        return 'Квадратичная'


class Cubic(Function):
    def make_function(self, X, Y):
        A = self.polinome_coef(X, Y, 3)
        self.function = self.function_from_coef(A)

    def __str__(self):
        return 'Кубическая'


class Forth(Function):
    def make_function(self, X, Y):
        A = self.polinome_coef(X, Y, 4)
        self.function = self.function_from_coef(A)

    def __str__(self):
        return '4 степени'


class Exponential(Function):
    def make_function(self, X, Y):
        a, b = self.polinome_coef(X, np.log(Y), 1)
        a = np.exp(a)
        x = sp.symbols('x')
        self.function = a * sp.exp(b * x)

    def __str__(self):
        return 'Экспоненциальная'


class Logarithmic(Function):
    def make_function(self, X, Y):
        b, a = self.polinome_coef(np.log(X), Y, 1)
        x = sp.symbols('x')
        self.function = a * sp.log(x) + b

    def __str__(self):
        return 'Логарифмическая'


class Power(Function):
    def make_function(self, X, Y):
        a, b = self.polinome_coef(np.log(X), np.log(Y), 1)
        a = np.exp(a)
        x = sp.symbols('x')
        self.function = a * x ** b

    def __str__(self):
        return 'Степенная'
