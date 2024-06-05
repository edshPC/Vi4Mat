import matplotlib.pyplot as plt
from Vi4Mat.Reader import *
from functions import *
from methods import *
import numpy as np

reader = Reader()
X, Y = [], []
func = None

if reader.fileMode or choice("как задать точки",
                             "через массив", "по графику") == "через массив":
    while True:
        print("Введите табличные значения как массив точек:")
        try:
            X = np.array([float(x) for x in reader.readline('X = ').split()])
            Y = np.array([float(x) for x in reader.readline('Y = ').split()])
        except Exception as e:
            print("Ошибка ввода:", e)
            continue
        if len(X) > 1 and len(X) == len(Y):
            break
        print("Длины массивов не совпадают или меньше 2")
else:
    func = choice("функцию, по которой найти массив точек:",
                  FunctionA(), FunctionB(), FunctionC(), FunctionD())
    while True:
        try:
            a, b = (float(x) for x in reader.readline("Введи интересующий интервал: ").split())
            n = reader.readnumber("Введи количество точек: ")
            if n < 2:
                raise Exception("Количество точек должно быть хотя бы 2")
            X = np.linspace(a, b, n)
            Y = func(X)
            break
        except Exception as e:
            print("Ошибка ввода:", e)

print("Значение в какой точке вычислить?")
x0 = reader.readnumber("x0 = ", float)

methods = [Lagrange(), NewtonDiv(), Gauss()]

for m in methods:
    m.calculate(X, Y)

print("Интерполяционные функции найдены")
for m in methods:
    print(f'{m}: f({x0}) = {m(x0)}')

if func is not None:
    print(f'Точное значение: f({x0}) = {func(x0)}')
    methods.append(func)

# График
bound_x = (X[1] - X[0]) / 5
a_x, b_x = X[0] - bound_x, X[-1] + bound_x

plt.plot(X, Y, 'o', markersize=8)

X_arr = np.linspace(a_x, b_x, 200)
X_arr = np.concatenate((X_arr, X))
X_arr.sort()

lw = 2
for m in methods:
    p = plt.plot(X_arr, m(X_arr), '--', linewidth=lw, label=str(m))
    plt.plot([x0], [m(x0)], 'o', markersize=lw * 4, color=p[0].get_color())
    lw -= 0.4

plt.grid(True)
plt.legend()
plt.show()
