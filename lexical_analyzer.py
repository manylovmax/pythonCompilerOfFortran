

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
            program_declared = False

            for line in lines:
                line = line.strip()
                if line.startswith('!'):
                    continue

                line_without_comments = line.split('!')[0]
                tokens = line_without_comments.split(' ')

                if not program_declared:
                    if len(tokens) != 2 or tokens[0] != 'program':
                        raise GrammaticalError('программа должна начинаться с "program" и имени программы')
                    else:
                        program_declared = True
                else:
                    pass
