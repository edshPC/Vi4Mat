import numpy as np


class Function:
    def f(self, x) -> float:
        pass

    def F(self, x) -> float:
        pass

    def check_bounds(self, a, b):
        return True

    def __call__(self, x):
        return self.f(x)


class FunctionA(Function):
    def f(self, x):
        return 1.5 * x ** 3 - 6.5 * x ** 2 + 2.5 * x + 7

    def F(self, x):
        return 1.5/4*x**4 - 6.5/3*x**3 + 2.5/2*x**2 + 7*x

    def __str__(self):
        return "f(x) = 1.5x^3 - 6.5x^2 + 2.5x + 7"


class FunctionB(Function):
    def f(self, x):
        return 2 * np.exp(x) - 5 * x ** 2 + 3 * x - 2

    def F(self, x):
        return 2 * np.exp(x) - 5/3 * x ** 3 + 3/2 * x**2 - 2*x

    def __str__(self):
        return "f(x) = 2e^x - 5x^2 + 3x - 2"


class FunctionC(Function):
    def f(self, x):
        return np.sin(x) + np.cos(2 * x) + np.exp(-x) - 0.5

    def F(self, x):
        return np.sin(2*x)/2 - np.cos(x) - np.exp(-x) - 0.5*x

    def __str__(self):
        return "f(x) = sin(x) + cos(2x) + exp(-x) - 0.5"


class FunctionD(Function):
    def f(self, x):
        return np.log(x) + 2 * np.sin(x)

    def F(self, x):
        return x*np.log(x) - 2 * np.cos(x) - x

    def check_bounds(self, a, b):
        return min(a, b) > 0

    def __str__(self):
        return "f(x) = ln(x) + 2sin(x)"

class FunctionE(Function):
    def f(self, x):
        return x ** 2

    def F(self, x):
        return x ** 3 / 3

    def __str__(self):
        return "f(x) = x^2"
