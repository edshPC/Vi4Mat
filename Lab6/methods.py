import numpy as np
from functions import Function


class Method:
    p = 1  # Порядок точности
    X = Y = epsilon = None

    def calculate(self, f: Function, x_0, x_n, y_0, h, epsilon):
        self.epsilon = epsilon
        Y0 = np.array([float('inf')])
        k = 0

        while True:
            self.X = X = np.arange(x_0, x_n + h, h)
            self.Y = Y1 = self.calculate_one(f, X, y_0, h)
            if self.accuracy(f, Y0, Y1) < epsilon:
                return k, self.accuracy(f, Y0, Y1)
            Y0 = Y1
            h /= 2
            k += 1

    def calculate_one(self, f, X, y_0, h):
        n = len(X)
        Y = np.zeros(n)
        Y[0] = y_0
        for i in range(n - 1):
            Y[i + 1] = self.next_step(f, h, X, Y, i)
        return Y

    def next_step(self, f: Function, h, X, Y, i):
        pass

    def accuracy(self, f: Function, Yh: np.ndarray, Yh2: np.ndarray):
        return abs(Yh[-1] - Yh2[-1]) / (2 ** self.p - 1)


class Euler(Method):
    def next_step(self, f: Function, h, X, Y, i):
        return Y[i] + h * f(X[i], Y[i])

    def __str__(self):
        return "Эйлера"


class RungeKutta4th(Method):
    p = 4

    def next_step(self, f: Function, h, X, Y, i):
        k1 = h * f(X[i], Y[i])
        k2 = h * f(X[i] + h / 2, Y[i] + k1 / 2)
        k3 = h * f(X[i] + h / 2, Y[i] + k2 / 2)
        k4 = h * f(X[i] + h, Y[i] + k3)
        return Y[i] + (k1 + 2 * k2 + 2 * k3 + k4) / 6

    def __str__(self):
        return "Рунге-Кутта IV"


class Milne(RungeKutta4th):
    p = 4

    def calculate_one(self, f, X, y_0, h):
        n = len(X)
        Y = np.zeros(n)
        Y[0] = y_0
        for i in range(min(3, n-1)):
            # Рунге-Кутта
            Y[i + 1] = super().next_step(f, h, X, Y, i)
        for i in range(3, n-1):
            Y[i + 1] = self.next_step(f, h, X, Y, i + 1)
        return Y

    def next_step(self, f: Function, h, X, Y, i):
        y_p = Y[i - 4] + 4 * h / 3 * (
                2 * f(X[i - 3], Y[i - 3]) -
                f(X[i - 2], Y[i - 2]) +
                2 * f(X[i - 1], Y[i - 1])
        )
        while True:
            y_k = Y[i - 2] + h / 3 * (
                    f(X[i - 2], Y[i - 2]) +
                    4 * f(X[i - 1], Y[i - 1]) +
                    f(X[i], y_p)
            )
            if abs(y_p - y_k) < self.epsilon:
                return y_k
            y_p = y_k

    def accuracy(self, f, Yh, Yh2):
        return np.max(np.abs(
            f.y(self.X, self.X[0], Yh2[0]) - Yh2
        ))

    def __str__(self):
        return "Милна"
