TOKENS_ADD_INDENT = ['program', 'if']


class GrammaticalError(Exception):
    error_text = None

    def __init__(self, error_text):
        self.error_text = error_text

    def __str__(self):
        return f'Грамматическая ошибка: {self.error_text}'


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

            for line in lines:
                if program_closed:
                    raise GrammaticalError('неверный токен - конец программы уже был объявлен')
                # очистка строки от пробелов в начале и конце
                stripped_line = line.strip()
                # очистить строку от комментариев
                line_without_comments = stripped_line.split('!')[0]
                tokens = line_without_comments.split(' ')
                # проверка на завершение блока
                if program_declared and stripped_line.startswith('end') and not program_closed:
                    if tokens[1] == 'program':
                        if not program_name == tokens[2]:
                            raise GrammaticalError('имя программы не верное')
                        else:
                            if len(tokens) == 3:
                                program_closed = True
                                continue
                            else:
                                raise GrammaticalError('только одно имя программы должно идти после end program')

                    elif tokens[1] == 'if' and open_indent_blocks[-1] == 'if':
                        open_indent_blocks.pop()

                    current_indent -= 2

                if current_indent:
                    # проверка на отсутп
                    for i in range(current_indent):
                        if line[i] != ' ':
                            raise GrammaticalError('неверный токен - должен быть отступ')
                    line = line[current_indent:]

                # если вся строка это комментарий - пропустить строку
                if line.startswith('!'):
                    continue

                # проверить на объявление модуля
                if not program_declared:
                    if len(tokens) != 2 or tokens[0] != 'program':
                        raise GrammaticalError('программа должна начинаться с "program" и имени программы')
                    else:
                        program_declared = True
                        program_name = tokens[1]
                        current_indent = 2
                else:
                    pass
