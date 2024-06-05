import matplotlib.pyplot as plt
from tabulate import tabulate
import numpy as np

from Vi4Mat.Reader import choice
from functions import *
from methods import *

func: Function = choice("ОДУ",
                        FunctionA(), FunctionB(), FunctionC())

while True:
    print("Введи исходные данные:")
    try:
        x_0 = float(input("x_0 = "))
        x_n = float(input("x_n = "))
        y_0 = float(input(f"y_0 = y({x_0}) = "))
        h = float(input("Шаг h = "))
        epsilon = float(input("Точность epsilon = "))
        assert h > 0 and x_0 + h <= x_n, "Должно быть хотя бы 1 разбиение"
        break
    except Exception as e:
        print("Ошибка ввода:", e)


methods = [Euler(), RungeKutta4th(), Milne()]
X = np.arange(x_0, x_n + h, h)
table = [
    ["Метод"] + [f'y({x:.1f})' for x in X] + ["Шаг", "epsilon"]
]

lw = 2
for m in methods:
    k, epsilon_real = m.calculate(func, x_0, x_n, y_0, h, epsilon)
    plt.plot(m.X, m.Y, '--', linewidth=lw, label=str(m))
    table.append(
        [str(m)] + m.Y[::2 ** k].tolist() + [h / 2 ** k, epsilon_real]
    )
    lw -= 0.4

table.append(["Точный"] + func.y(X, x_0, y_0).tolist())
print(tabulate(table, headers="firstrow", tablefmt="github", floatfmt=".5f"))

X = np.linspace(x_0, x_n, 200)
plt.plot(X, func.y(X, x_0, y_0), '--', linewidth=lw, label="Точное")

plt.grid(True)
plt.legend()
plt.show()
