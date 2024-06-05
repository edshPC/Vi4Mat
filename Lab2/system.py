import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from Vi4Mat.Reader import choice


class System:
    f_data = None
    g_data = None
    f = None
    g = None
    dfdx = None
    dfdy = None
    dgdx = None
    dgdy = None

    def __init__(self, interest):
        self.interest = interest

    def __str__(self):
        return f"System:\n    f(x,y): {self.f_data} = 0\n    g(x,y): {self.g_data} = 0"

    def init(self):
        x, y = sp.symbols('x y')
        self.f = sp.lambdify([x, y], self.f_data)
        self.g = sp.lambdify([x, y], self.g_data)
        self.dfdx = sp.lambdify([x, y], sp.diff(self.f_data, x))
        self.dfdy = sp.lambdify([x, y], sp.diff(self.f_data, y))
        self.dgdx = sp.lambdify([x, y], sp.diff(self.g_data, x))
        self.dgdy = sp.lambdify([x, y], sp.diff(self.g_data, y))

    def graph(self):
        X, Y = np.meshgrid(
            np.linspace(*self.interest[0], 100),
            np.linspace(*self.interest[1], 100)
        )
        plt.contour(X, Y, self.f(X, Y), [0], colors=['g'])
        plt.contour(X, Y, self.g(X, Y), [0], colors=['r'])

        plt.title('Посмотри на график и запомни начальное приближение корней')
        plt.grid(True)
        plt.show()


class SystemA(System):
    def __init__(self):
        x, y = sp.symbols('x y')
        self.f_data = sp.tan(x * y) - x ** 2
        self.g_data = 0.8 * x ** 2 + 2 * y ** 2 - 1
        super().__init__([[-2, 2], [-2, 2]])


class SystemB(System):
    def __init__(self):
        x, y = sp.symbols('x y')
        self.f_data = x ** 2 - 3 * y ** 2 - 2
        self.g_data = 0.8 * x ** 2 + 2 * y ** 2 - 9
        super().__init__([[-5, 5], [-5, 5]])


def calculate_system(system, x0, y0, accuracy):
    x, y = x0, y0
    error = None
    max_iters = 1000  # Максимальное количество итераций
    k = 0
    while True:
        # матрица Якоби
        jacobian = np.array([
            [system.dfdx(x, y), system.dfdy(x, y)],
            [system.dgdx(x, y), system.dgdy(x, y)]
        ])
        det = np.linalg.det(jacobian)
        if det == 0:
            print("Матрица Якоби вырождена")
            break

        # обратная матрица Якоби
        inv_jacobian = np.linalg.inv(jacobian)

        B = - np.array([
            system.f(x, y), system.g(x, y)
        ])
        # матрица дельт = J^-1 * X
        delta = np.dot(inv_jacobian, B)

        print("Решаем систему:")
        print(f'{jacobian[0][0]:.2f} dx + {jacobian[0][1]:.2f} dy = {B[0]:.2f}')
        print(f'{jacobian[1][0]:.2f} dx + {jacobian[1][1]:.2f} dy = {B[1]:.2f}')
        print(f'dx, dy = {delta[0]:.4f}, {delta[1]:.4f}')

        x = x + delta[0]
        y = y + delta[1]

        print(f'x, y = {x:.4f}, {y:.4f}')

        error = abs(delta)
        if max(error) < accuracy:
            break
        k += 1
        if k > max_iters:
            print("Итерации расходятся!")
            break

    return (x, y), error, k


system = choice("систему уравнений",
                SystemA(), SystemB())
system.init()
system.graph()
print("Введи начальное приближение:")
x0 = float(input("x0 = "))
y0 = float(input("y0 = "))
accuracy = float(input("Введи точность: "))
answer, error, iters = calculate_system(system, x0, y0, accuracy)
x, y = answer
print("Найденное решение:")
print(f'x = {x}')
print(f'y = {y}')
print(f'f(x,y) = {system.f(x, y)}')
print(f'g(x,y) = {system.g(x, y)}')
print("Вектор погрешности:")
print(error)
print("Итераций затрачено:", iters)
