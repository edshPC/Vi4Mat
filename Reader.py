def choice(prompt, *variants):
    print("Выбери", prompt)
    choices = {str(i + 1): variants[i] for i in range(len(variants))}
    for k, v in choices.items():
        print(f'{k}. {v}')
    ans = None
    while ans not in choices:
        ans = input("Введи номер: ")
    return variants[int(ans) - 1]


class Reader:
    def __init__(self):
        self.fileMode = choice("способ ввода", "консоль", "файл") == "файл"
        while self.fileMode:
            try:
                fileName = input("Путь к файлу: ")
                self.file = open(fileName, 'r+', encoding='utf-8')
                break
            except Exception:
                print("Файл не найден")

    def readline(self, prompt=''):
        print(prompt, end='')
        if (self.fileMode):
            line = self.file.readline()
            if len(line) == 0:
                print("Достигнут конец файла, читать нечего")
                exit(-1)
            print(line, end='')
            return line
        return input()

    def readnumber(self, prompt='', function=int):
        while True:
            try:
                return function(self.readline(prompt))
            except Exception:
                pass

    def print(self, *args):
        print(*args)
        if self.fileMode:
            self.file.write(" ".join(map(str, args)) + "\n")

    def close(self):
        if self.fileMode:
            self.file.close()
