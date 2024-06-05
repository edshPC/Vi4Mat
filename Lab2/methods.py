import numpy as np


class Method:
    def __init__(self, needs_aprx, needs_cond):
        self.needs_aprx = needs_aprx
        self.needs_cond = needs_cond
        self.bounds = None
        self.accuracy = None
        self.iters = None
        self.answer = None

    def validate(self, func):
        if self.needs_aprx:
            return True
        a, b = self.bounds
        if func(a) * func(b) > 0:  # если одинаковые знаки на концах
            return False
        sign = func(a) > 0
        sign_changes = 0
        for x in np.linspace(a, b, 100):
            if (func(x) > 0) != sign:  # если знак не совпал с прошлым
                sign_changes += 1
                sign = func(x) > 0
                if sign_changes > 1:  # Если функция меняет знак более 1 раза
                    return False
        return True

    def convergence_condition(self, func):
        return True

    def calculate(self, func):
        pass



class HalfDivision(Method):
    def __init__(self):
        super().__init__(False, False)

    def __str__(self):
        return "Метод половинного деления"

    def calculate(self, func):
        self.iters = 0
        a, b = self.bounds
        x = (a + b) / 2
        while abs(func(x)) > self.accuracy or abs(a - b) > self.accuracy:
            x = (a + b) / 2
            if func(a) * func(x) > 0:
                a = x
            else:
                b = x
            self.iters += 1
        self.answer = (a + b) / 2


class Newton(Method):
    def __init__(self):
        super().__init__(True, False)

    def __str__(self):
        return "Метод Ньютона"

    def calculate(self, func):
        self.iters = 0
        a, b = self.bounds
        if func(a) * func.df2(a) > 0:
            x = a  # Начальное приближение
        else:
            x = b
        while abs(func(x)) > self.accuracy:
            x = x - func.f(x) / func.df(x)
            self.iters += 1
        self.answer = x


class SimpleIteration(Method):
    def __init__(self):
        super().__init__(False, True)

    def __str__(self):
        return "Метод простой итерации"

    def convergence_condition(self, func):  # Условие сходимости
        a, b = self.bounds
        func.set_lambda(a, b)
        print(f'phi\'(a,b) = {func.dphi(a):.4f}, {func.dphi(b):.4f}')
        return max(abs(func.dphi(x)) for x in self.bounds) < 1

    def calculate(self, func):
        self.iters = 0
        a, b = self.bounds
        func.set_lambda(a, b)
        x0 = (a + b) / 2  # Начальное приближение
        max_iters = 100

        while True:
            self.iters += 1
            x1 = func.phi(x0)  # Вычисляем следующее приближение
            if abs(x1 - x0) < self.accuracy:
                break
            x0 = x1
            if self.iters > max_iters or abs(x0) > 1e10:
                print("Итерации расходятся!!!")
                break

        self.answer = x0

