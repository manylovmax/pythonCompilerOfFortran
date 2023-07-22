import string

TOKENS_ADD_INDENT = ['program', 'if']
TOKEN_ALLOWED_SYMBOLS = string.ascii_letters + string.digits


class GrammaticalError(Exception):
    error_text = None
    line_number = None
    symbol_number = None

    def __init__(self, error_text, line_number, symbol_number):
        self.error_text = error_text
        self.line_number = line_number
        self.symbol_number = symbol_number

    def __str__(self):
        return f'{self.line_number}:{self.symbol_number} Грамматическая ошибка: {self.error_text}'


class LexicalAnalyzer:
    program_filename = None

    def __init__(self, program_filename):
        self.program_filename = program_filename

    def analyze(self):
        with open(self.program_filename, 'r') as f:
            lines = f.readlines()
            # в текущей реализации в файле может быть только один модуль
            program_declared = False
            program_closed = False
            program_name = None
            current_indent = 0
            open_indent_blocks = []
            line_number = 0
            symbol_number = 0

            for line in lines:
                line_number += 1
                if program_closed:
                    raise GrammaticalError('неверный токен - конец программы уже был объявлен', line_number, symbol_number)
                # очистить строку от комментариев
                line_without_comments = line.split('!')[0]
                # обработка строки посимвольно
                for c in line_without_comments:
                    pass
                tokens = line_without_comments.split(' ')
                # проверка на завершение блока
                if program_declared and line.startswith('end') and not program_closed:
                    if tokens[1] == 'program':
                        if not program_name == tokens[2]:
                            raise GrammaticalError('имя программы не верное', line_number, symbol_number)
                        else:
                            if len(tokens) == 3:
                                program_closed = True
                                continue
                            else:
                                raise GrammaticalError('только одно имя программы должно идти после end program', line_number, symbol_number)

                    elif tokens[1] == 'if' and open_indent_blocks[-1] == 'if':
                        open_indent_blocks.pop()

                    current_indent -= 2

                if current_indent:
                    # проверка на отсутп
                    for i in range(current_indent):
                        if line[i] != ' ':
                            raise GrammaticalError('неверный токен', line_number, symbol_number)
                        symbol_number += 1
                    line = line[current_indent:]
                    symbol_number = current_indent

                # если вся строка это комментарий - пропустить строку
                if line.startswith('!'):
                    continue

                # проверить на объявление модуля
                if not program_declared:
                    if len(tokens) != 2 or tokens[0] != 'program':
                        raise GrammaticalError('программа должна начинаться с "program" и имени программы', line_number, symbol_number)
                    else:
                        program_declared = True
                        program_name = tokens[1].strip()
                        current_indent = 2
                else:
                    pass
