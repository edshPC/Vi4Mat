import matplotlib.pyplot as plt
from Vi4Mat.Reader import Reader
from functions import *
from tabulate import tabulate

reader = Reader()

while True:
    print('Введите табличные значения как массив точек:')
    try:
        X = np.array([float(x) for x in reader.readline('X = ').split()]) / 30
        Y = np.array([float(x) for x in reader.readline('Y = ').split()])
    except Exception as e:
        print("Ошибка ввода:", e)
        continue
    if len(X) > 1 and len(X) == len(Y):
        break
    print('Длины массивов не совпадают или меньше 2')

n = len(X)
functions = [Linear(), Quadratic(), Cubic(), # Forth(),
             Exponential(), Logarithmic(), Power()]

for f in functions:
    f.make_lambda(X, Y)
    f.phi = f(X)
    f.epsilon = f.phi - Y
    f.S = np.sum(f.epsilon ** 2)
    f.SKO = np.sqrt(f.S / n)
    f.phi_avg = np.sum(f.phi) / n
    f.R2 = 1 - f.S / np.sum((Y - f.phi_avg) ** 2)

functions = [f for f in functions if f.valid]
best = min(functions, key=lambda f: f.SKO)

X_avg = np.sum(X) / n
Y_avg = np.sum(Y) / n
r = np.sum((X - X_avg) * (Y - Y_avg)) / np.sqrt(np.sum((X - X_avg) ** 2) * np.sum((Y - Y_avg) ** 2))
print("Коэффициент корреляции Пирсона:", r)

table = [
    ['i'] + list(range(1, n + 1)),
    ['X'] + X.tolist(),
    ['Y'] + Y.tolist()
]
for f in functions:
    table.extend([
        [str(f)],
        ['phi(X)'] + f.phi.tolist(),
        ['epsilon'] + f.epsilon.tolist()
    ])
print("Результаты аппроксимации:")
print(tabulate(table, headers="firstrow", tablefmt="github", floatfmt=".3f"))
print()


def apprx_type(R2):
    if R2 >= 0.95:
        return "Высокая"
    if R2 >= 0.75:
        return "Удовлетворительная"
    if R2 >= 0.5:
        return "Слабая"
    return "Недостаточная"


table = [
    ["Вид функции", "Мера отклонения S", "СКО 𝜹", "Достоверность R^2", "Точность аппроксимации"]
]
for f in functions:
    table.append([
        str(f), f.S, f.SKO, f.R2, apprx_type(f.R2)
    ])
print("Сравнение аппроксимирующих функций:")
print(tabulate(table, headers="firstrow", tablefmt="github", floatfmt=".5f"))
print()
print("Лучшая функция:", best)
print("phi(x) =", best.function)

# График
a_x, b_x = min(X), max(X)
bound = (b_x - a_x) / 10
a_x, b_x = a_x - bound, b_x + bound

plt.plot(X, Y, 'o', markersize=8)

X_arr = np.linspace(a_x, b_x, 200)
for f in functions:
    if f is best:
        plt.plot(X_arr, f(X_arr), linewidth=2, label=str(f))
    else:
        plt.plot(X_arr, f(X_arr), '--', label=str(f))

plt.grid(True)
plt.legend()
plt.show()
