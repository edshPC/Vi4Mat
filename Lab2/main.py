from functions import *
from Vi4Mat.Reader import *
from methods import *


func = choice("функцию для решения",
              FunctionA(), FunctionB(), FunctionC(), FunctionD())
method = choice("метод решения",
                HalfDivision(), Newton(), SimpleIteration())

func.graph()
print("Ввод исходных данных")
reader = Reader()
while True:
    try:
        method.bounds = tuple(map(float, reader.readline("Введи интересующий промежуток: ").split()))
    except Exception as e:
        print("Ошибка ввода:", e)
        continue
    if not func.check_bounds(*method.bounds):
        print("Границы за пределами области определения")
        continue
    if len(method.bounds) == 2 and method.validate(func):
        break
    print("Условие единственности корня не выполнено")
    if reader.fileMode:
        exit()
    func.graph()

method.accuracy = reader.readnumber("Введи точность: ", float)

if not method.convergence_condition(func):
    print("Условие сходимости метода не выполнено!")

method.calculate(func)
reader.print("Найденное решение:")
reader.print("x =", method.answer)
reader.print("f(x) =", func(method.answer))
reader.print("Итераций затрачено:", method.iters)

