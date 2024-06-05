import math

import numpy as np
import sympy as sp
from functools import lru_cache
from tabulate import tabulate

x = sp.symbols('x')


class Method:
    function = None
    lmb = None
    X, Y = [], []

    def polinome_coef(self, X, Y) -> np.ndarray:
        pass

    def make_function(self, X, Y):
        A = self.polinome_coef(X, Y)
        self.function = sum(A[i] * x ** i for i in range(len(A)))

    def lambdify(self):
        self.lmb = sp.lambdify(x, self.function)

    def calculate(self, X, Y):
        self.X, self.Y = X, Y
        self.make_function(X, Y)
        self.lambdify()

    def __call__(self, *args):
        return self.lmb(*args)


class Lagrange(Method):
    def polinome_coef(self, X, Y):  # Решение через систему уравнений (не используется)
        n = len(X)
        M = np.column_stack([X ** j for j in range(n)])
        A = np.linalg.solve(M, Y)
        return A

    def make_function(self, X, Y):
        n = len(X)
        L = sum(
            Y[i] * np.prod([
                (x - X[j]) / (X[i] - X[j]) for j in range(n) if j != i
            ]) for i in range(n)
        )
        self.function = L

    def __str__(self):
        return "Лагранж"


class NewtonDiv(Method):
    def make_function(self, X, Y):
        n = len(X)
        N = sum(
            self.divided_diff(0, k)
            * np.prod([
                x - X[j] for j in range(k)
            ]) for k in range(n)
        )
        self.function = N

    @lru_cache()
    def divided_diff(self, left, right):
        if left == right:
            return self.Y[left]
        return ((self.divided_diff(left + 1, right) - self.divided_diff(left, right - 1))
                / (self.X[right] - self.X[left]))

    def __str__(self):
        return "Ньютон с разд. разностями"


class Gauss(Method):
    def make_function(self, X, Y):
        n = len(X) - 1  # Количество рабиений = 2n
        a = X[n // 2]
        h = (X[-1] - X[0]) / n
        if n % 2 or h != X[1] - X[0]:
            print("Количество точек чётно или точки не равностоящие!\nМетод Гаусса может быть неточным")
        t = (x - a) / h
        # Первая интерполяционная формула Гаусса
        P1 = sum(
            np.prod([
                t + j for j in range(-(i // 2), (i + 1) // 2)
            ]) / math.factorial(i)
            * self.finite_diff(-(i // 2), i)
            for i in range(n + 1)
        )
        # Вторая интерполяционная формула Гаусса
        P2 = sum(
            np.prod([
                t - j for j in range(-(i // 2), (i + 1) // 2)
            ]) / math.factorial(i)
            * self.finite_diff(-((i + 1) // 2), i)
            for i in range(n + 1)
        )
        self.function = P1, P2

        # Вывод конечных разностей
        table = [
            ['Xi', 'Yi'] + [f'Δ^{i}Yi' for i in range(1, n + 1)]
        ] + [
            [f'X{i}'] + [self.finite_diff(i, j) for j in range(0, (n + 1) // 2 + 1 - i)]
            for i in range(-(n // 2), (n + 1) // 2 + 1)
        ]
        print("Таблица конечных разностей функции:")
        print(tabulate(table, headers="firstrow", tablefmt="github", floatfmt=".2f"))

    def lambdify(self):
        P1, P2 = self.function
        lmb1, lmb2 = sp.lambdify(x, P1), sp.lambdify(x, P2)
        n = len(self.X) - 1  # Количество рабиений = 2n
        a = self.X[n // 2]
        self.lmb = np.vectorize(lambda x: lmb1(x) if x > a else lmb2(x))

    @lru_cache()
    def finite_diff(self, i, k):
        if k == 0:
            return self.Y[i + (len(self.Y) - 1) // 2]
        return self.finite_diff(i + 1, k - 1) - self.finite_diff(i, k - 1)

    def __str__(self):
        return "Гаусс"
