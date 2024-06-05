import numpy as np


class Method:
    k = 1  # Порядок точности правила Рунге

    def runge_rule(self, Ih, Ih2):
        return abs(Ih2 - Ih) / (2 ** self.k - 1)

    def calculate_one(self, func, x_array, h) -> float:
        pass

    def calculate(self, func, a, b, accuracy):
        n = 4
        I0 = float('inf')
        while True:
            h = (b - a) / n
            x_array = np.linspace(a, b, n + 1)
            I1 = self.calculate_one(func, x_array, h)
            #print(n, I1, self.runge_rule(I0, I1))
            if self.runge_rule(I0, I1) < accuracy:
                return I1, n
            I0 = I1
            n *= 2

    def accurate(self, func, a, b):
        return func.F(b) - func.F(a)


class LeftRectangle(Method):
    def calculate_one(self, func, x_array, h):
        return sum(func(x_array[:-1])) * h

    def __str__(self):
        return "Метод левых прямоугольников"


class RightRectangle(Method):
    def calculate_one(self, func, x_array, h):
        return sum(func(x_array[1:])) * h

    def __str__(self):
        return "Метод правых прямоугольников"


class Midpoint(Method):
    k = 2

    def calculate_one(self, func, x_array, h):
        # Матричное суммирование numpy
        centers = (x_array[:-1] + x_array[1:]) / 2
        return h * sum(func(centers))

    def __str__(self):
        return "Метод средних прямоугольников"


class Trapezoidal(Method):
    k = 2

    def calculate_one(self, func, x_array, h):
        return h * (
                (func(x_array[0]) + func(x_array[-1])) / 2 +
                sum(func(x_array[1:-1]))
        )

    def __str__(self):
        return "Метод трапеций"


class Simpson(Method):
    k = 4

    def calculate_one(self, func, x_array, h):
        return h / 3 * (
                func(x_array[0]) +  # y0
                4 * sum(func(x_array[1:-1:2])) +  # y1 + y3 + ... + yn-1
                2 * sum(func(x_array[2:-2:2])) +  # y2 + y4 + ... + yn-2
                func(x_array[-1])  # yn
        )

    def __str__(self):
        return "Метод Симпсона"
