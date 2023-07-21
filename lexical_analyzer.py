PROGRAM_FILE_NAME = 'program.f'


class GrammaticalError(Exception):
    error_text = None

    def __init__(self, error_text):
        self.error_text = error_text

    def __str__(self):
        return f'Грамматическая ошибка: {self.error_text}'

class LexicalAnalyzer:

    def __init__(self):
        pass


    def read_file(self):
        with open(PROGRAM_FILE_NAME) as f:
            lines = f.readlines()
            for line in lines:
                tokens = line.split(' ')
                if len(tokens) != 2:
                    raise GrammaticalError('программа должна начинаться с "program" и имени программы')