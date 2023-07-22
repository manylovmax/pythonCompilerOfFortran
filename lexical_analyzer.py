import string
from enum import Enum

TOKENS_ADD_INDENT = ['program', 'if']
TOKEN_ALLOWED_SYMBOLS = string.ascii_letters + string.digits


class TokenConstructions(Enum):
    PROGRAM_DECLARATION = 1
    END_DECLARATION_START = 2
    NEW_TOKEN = 3


class GrammaticalError(Exception):
    error_text = None
    line_number = None
    symbol_number = None

    def __init__(self, error_text, line_number, current_character_number):
        self.error_text = error_text
        self.line_number = line_number
        self.current_character_number = current_character_number

    def __str__(self):
        return f'строка {self.line_number} символ {self.current_character_number}: Грамматическая ошибка: {self.error_text}'


class LexicalAnalyzer:
    program_filename = None
    current_state = None

    def __init__(self, program_filename):
        self.program_filename = program_filename
        self.current_state = TokenConstructions.NEW_TOKEN

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
            current_character_number = 0

            for line in lines:
                current_character_number = 0
                line_number += 1
                if program_closed:
                    raise GrammaticalError('неверный токен - конец программы уже был объявлен', line_number, current_character_number)
                # очистить строку от комментариев
                line_without_comments = line.split('!')[0]
                # если вся строка это комментарий - пропустить строку
                if line.startswith('!'):
                    continue

                # обработка строки посимвольно
                current_token = ''
                current_token_number = 1
                for c in line_without_comments:
                    if current_indent and current_character_number < current_indent:
                        pass
                    else:
                        # проверка первого символа
                        if c not in string.ascii_letters and current_character_number == current_indent:
                            raise GrammaticalError("недопустимый символ", line_number, current_character_number)
                        # сборка токена
                        if c != ' ' and c != '\n':
                            current_token += c
                        if (c == ' ' or c == '\n') and current_token:
                            current_token_lower = current_token.lower()
                            if current_token_lower == 'program':
                                if program_declared and current_token_number == 1:
                                    raise GrammaticalError("недопустимый символ", line_number, current_character_number)
                                self.current_state = TokenConstructions.PROGRAM_DECLARATION
                                current_token = current_token_lower = ''
                            elif self.current_state == TokenConstructions.PROGRAM_DECLARATION:
                                if current_token_number == 2:
                                    program_name = current_token
                                    current_indent += 2
                                    open_indent_blocks.append('program')
                                    current_token = current_token_lower = ''
                                    self.current_state = TokenConstructions.NEW_TOKEN
                                else:
                                    raise GrammaticalError("недопустимый символ", line_number, current_character_number)
                            elif current_token_lower == 'end':
                                self.current_state = TokenConstructions.END_DECLARATION_START
                                current_token = current_token_lower = ''
                            elif self.current_state == TokenConstructions.END_DECLARATION_START:
                                if current_token_lower == 'program':
                                    program_closed = True
                                elif current_token_lower == 'if' and open_indent_blocks[-1] == 'if':
                                    current_indent -= 2
                                    open_indent_blocks.pop()
                                    self.current_state = TokenConstructions.NEW_TOKEN
                                    current_token = current_token_lower = ''
                            elif self.current_state == TokenConstructions.NEW_TOKEN:
                                    current_token = current_token_lower = ''



                            current_token_number += 1

                    current_character_number += 1
