import numpy as np

class Function:
    def f(self, x):
        pass

    def __call__(self, *args):
        return self.f(*args)


class FunctionA(Function):
    def f(self, x):
        return 1.5 * x ** 3 - 6.5 * x ** 2 + 2.5 * x + 7

    def __str__(self):
        return "f(x) = 1.5x^3 - 6.5x^2 + 2.5x + 7"


class FunctionB(Function):
    def f(self, x):
        return 2 * np.exp(x) - 5 * x ** 2 + 3 * x - 2

    def __str__(self):
        return "f(x) = 2e^x - 5x^2 + 3x - 2"


class FunctionC(Function):
    def f(self, x):
        return np.sin(x) + np.cos(2 * x) + np.exp(-x) - 0.5

    def __str__(self):
        return "f(x) = sin(x) + cos(2x) + exp(-x) - 0.5"


class FunctionD(Function):
    def f(self, x):
        return 2 * np.sin(x)

    def __str__(self):
        return "f(x) = 2sin(x)"
