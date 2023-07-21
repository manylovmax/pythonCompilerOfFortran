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
            line_number = 0
            for line in lines:
                line_number += 1
                tokens = line.split(' ')

                if line_number == 1:
                    if len(tokens) != 2:
                        raise GrammaticalError('программа должна начинаться с "program" и имени программы')
                else:
                    pass
