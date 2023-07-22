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
            current_indent = 0

            for line in lines:
                if current_indent:
                    # проверка на отсутп
                    i = 0
                    for i in range(current_indent):
                        if line[i] != ' ':
                            raise GrammaticalError('неверный токен - должен быть отступ')
                    line = line[current_indent:]

                # если вся строка это комментарий - пропустить строку
                if line.startswith('!'):
                    continue

                # очистить строку от комментариев
                line_without_comments = line.split('!')[0]
                tokens = line_without_comments.split(' ')
                # проверить на объявление модуля
                if not program_declared:
                    if len(tokens) != 2 or tokens[0] != 'program':
                        raise GrammaticalError('программа должна начинаться с "program" и имени программы')
                    else:
                        program_declared = True
                else:
                    pass
