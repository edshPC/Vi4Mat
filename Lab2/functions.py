import matplotlib.pyplot as plt
import numpy as np


class Function:
    lmb = 1

    def __init__(self, *interest):
        self.interest = interest

    def f(self, x) -> float:
        pass

    def df(self, x) -> float:
        pass

    def df2(self, x) -> float:
        pass

    def phi(self, x) -> float:
        return x + self.lmb * self.f(x)

    def dphi(self, x) -> float:
        return 1 + self.lmb * self.df(x)

    def set_lambda(self, a, b):
        self.lmb = 1 / max(abs(self.df(a)), abs(self.df(b)))
        if self.df(a) > 0:
            self.lmb *= -1

    def check_bounds(self, a, b):
        return True

    def graph(self):
        x = np.linspace(*self.interest, 100)
        plt.plot(x, self(x))
        plt.axhline(y=0, color='k', linewidth=1)
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.title(f'Посмотри на график и запомни границы поиска корня\n{self}')
        plt.grid(True)
        plt.show()

    def __call__(self, x):
        return self.f(x)


class FunctionA(Function):
    def __init__(self):
        super().__init__(-2, 5)

    def f(self, x):
        return 1.5 * x ** 3 - 6.5 * x ** 2 + 2.5 * x + 7

    def df(self, x):
        return 4.5 * x ** 2 - 13 * x + 2.5

    def df2(self, x):
        return 9 * x - 13

    def __str__(self):
        return "f(x) = 1.5x^3 - 6.5x^2 + 2.5x + 7"


class FunctionB(Function):
    def __init__(self):
        super().__init__(-2, 4)

    def f(self, x):
        return 2 * np.exp(x) - 5 * x ** 2 + 3 * x - 2

    def df(self, x):
        return 2 * np.exp(x) - 10 * x + 3

    def df2(self, x):
        return 2 * np.exp(x) - 10

    def __str__(self):
        return "f(x) = 2e^x - 5x^2 + 3x - 2"


class FunctionC(Function):
    def __init__(self):
        super().__init__(0, 5)

    def f(self, x):
        return np.sin(x) + np.cos(2 * x) + np.exp(-x) - 0.5

    def df(self, x):
        return np.cos(x) - 2 * np.sin(2 * x) - np.exp(-x)

    def df2(self, x):
        return -np.sin(x) - 4 * np.cos(2 * x) + np.exp(-x)

    def __str__(self):
        return "f(x) = sin(x) + cos(2x) + exp(-x) - 0.5"


class FunctionD(Function):
    def __init__(self):
        super().__init__(0.1, 6)

    def f(self, x):
        return np.log(x) + 2 * np.sin(x)

    def df(self, x):
        return 1 / x + 2 * np.cos(x)

    def df2(self, x):
        return -1 / (x ** 2) - 2 * np.sin(x)

    def check_bounds(self, a, b):
        return min(a, b) > 0

    def __str__(self):
        return "f(x) = ln(x) + 2sin(x)"
