import numpy as np


class Function:
    def f(self, x: float | np.ndarray, y):
        """y' = f(x, y)"""

    def y(self, x: float | np.ndarray, x_0, y_0):
        """y = f(x) - точное решение задачи Коши в y(x_0) = y_0"""

    def __call__(self, *args):
        return self.f(*args)


class FunctionA(Function):
    def f(self, x, y):
        return 1 + 3 * y + 2 * x ** 2

    def y(self, x, x_0, y_0):
        C = (y_0 + 2 / 3 * x_0 ** 2 + 4 / 9 * x_0 + 13 / 27) / np.exp(3 * x_0)
        return C * np.exp(3 * x) - 2 / 3 * x ** 2 - 4 / 9 * x - 13 / 27

    def __str__(self):
        return "y' = 1 + 3y + 2x^2"


class FunctionB(Function):
    def f(self, x, y):
        return y * np.tan(x) - x ** 2

    def y(self, x, x_0, y_0):
        C = (y_0 + 2 * x_0) * np.cos(x_0) + (x_0 ** 2 - 2) * np.sin(x_0)
        return (C - (x ** 2 - 2) * np.sin(x)) / np.cos(x) - 2 * x

    def __str__(self):
        return "y' = y*tg(x) - x^2"


class FunctionC(Function):
    def f(self, x, y):
        return 2 * y + 3 * np.sin(2 * x) - np.cos(x)

    def y(self, x, x_0, y_0):
        C = (y_0 + 3 / 4 * (np.sin(2 * x_0) + np.cos(2 * x_0)) + 1 / 5 * (np.sin(x_0) - 2 * np.cos(x_0))) / np.exp(2 * x_0)
        return - 3 / 4 * (np.sin(2 * x) + np.cos(2 * x)) - 1 / 5 * (np.sin(x) - 2 * np.cos(x)) + C * np.exp(2 * x)

    def __str__(self):
        return "y' = 2y + 3sin(2x) - cos(x)"
