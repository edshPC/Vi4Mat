from functions import *
from methods import *
from Vi4Mat.Reader import choice


func = choice("функцию для решения",
              FunctionA(), FunctionB(), FunctionC(), FunctionD(), FunctionE())
method = choice("метод решения",
                LeftRectangle(), RightRectangle(), Midpoint(), Trapezoidal(), Simpson())

print("Ввод исходных данных")
while True:
    try:
        a, b = map(float, input("Введи интересующий промежуток: ").split())
    except Exception as e:
        print("Ошибка ввода:", e)
        continue
    if func.check_bounds(a, b):
        break
    print("Границы за пределами области определения")

accuracy = float(input("Введи точность: "))

I, n = method.calculate(func, a, b, accuracy)
Iacc = method.accurate(func, a, b)

print("Найденное решение:")
print(f'{a}\n ∫ f(x)dx = {I}\n{b}')
print("Разбиений потребовалось:", n)
print("Точное решение: Iacc =", Iacc)
print("|I - Iacc| =", abs(I - Iacc))

