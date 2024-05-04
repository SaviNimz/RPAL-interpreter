from enum import Enum

PUNCTUATION = ['(', ')', ';', ',']

# to identify the reservered keywords
RESERVED_KEYWORDS = ['fn','where', 'let', 'aug', 'within' ,'in' ,'rec' ,'eq','gr','ge','ls','le','ne','or','@','not','&','true','false','nil','dummy','and','|']
class Token():
    def __init__(self, type, value):
        self.type = type
        self.value = value

class TokenType(Enum):
    RESERVED_KEYWORD = 'RESERVED_KEYWORD'
    ID = 'ID'
    COMMENT = 'COMMENT'
    INT = 'INT'
    COMMA = 'COMMA'
    PLUS = 'PLUS'  
    MINUS = 'MINUS' 
    MUL = 'MUL'  
    DIV = 'DIV'  
    GREATER_THAN = 'GREATER_THAN' 
    LESSER_THAN = 'LESSER_THAN'  
    AMPERSAND_OPERATOR = 'AMPERSAND_OPERATOR'
    DOT_OPERATOR = 'DOT_OPERATOR'  
    AT_OPERATOR = 'AT_OPERATOR' 
    SEMICOLON = 'SEMICOLON' 
    EQUAL = 'EQUAL' 
    CURL = 'CURL' 
    SQUARE_OPEN_BRACKET = 'SQUARE_OPEN_BRACKET' 
    SQUARE_CLOSE_BRACKET = 'SQUARE_CLOSE_BRACKET' 
    DOLLAR = 'DOLLAR' 
    EXCLAMATION_MARK = 'EXCLAMATION_MARK'
    HASH_TAG = 'HASH_TAG'
    MODULUS = 'MODULUS'
    CARROT = 'CARROT'
    CURLY_OPEN_BRACKET = 'CURLY_OPEN_BRACKET'
    CURLY_CLOSE_BRACKET = 'CURLY_CLOSE_BRACKET'
    BACK_TICK = 'BACK_TICK'
    DOUBLE_QUOTE = 'DOUBLE_QUOTE'
    QUESTION_MARK = 'QUESTION_MARK'
    PUNCTUATION = 'PUNCTUATION'
    OR_OPERATOR = 'OR_OPERATOR'
    STRING = 'STRING'
    TERNARY_OPERATOR = 'TERNARY_OPERATOR'
    GREATER_THAN_OR_EQUAL = 'GREATER_THAN_OR_EQUAL'
    LESSER_THAN_OR_EQUAL = 'LESSER_THAN_OR_EQUAL'
    POWER = 'POWER'
    EOF = 'EOF'


class LEX_STATE:
    def __init__(self):
        self.line_number = 0
        self.current_char = None
        self.column_number = None


class Tokenizer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.state = LEX_STATE()

        self.state.current_char = self.text[self.pos]
        self.state.line_number = 1
        self.state.column_number = 1

    def error(self):
        raise Exception('Error parsing input')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.state.current_char = None  # Indicates end of input
        else:
            self.state.current_char = self.text[self.pos]
            self.state.column_number += 1

    def skip_whitespace(self):
        while self.state.current_char is not None and self.state.current_char.isspace():
            if self.state.current_char == '\n':
                self.state.line_number += 1
                self.state.column_number = 0
            self.advance()

    def integer(self):
        result = ''
        while self.state.current_char is not None :
            if self.state.current_char.isdigit():
                result += self.state.current_char
                self.advance()
            elif self.state.current_char.isalpha():
                self.error()
            else: break


        return int(result)

    def identifier(self):
        result = ''
        while self.state.current_char is not None and (
                self.state.current_char.isalpha() or self.state.current_char.isdigit() or self.state.current_char == '_'):
            result += self.state.current_char
            self.advance()
        return result

    def comment(self):
        result = ''
        while self.state.current_char is not None and self.state.current_char != '\n':
            result += self.state.current_char
            self.advance()
        return result

    def string(self):
        result = ''
        while self.state.current_char is not None and self.state.current_char != "'":
            result += self.state.current_char
            self.advance()
        self.advance()
        return result

    def get_next_token(self):
        while self.state.current_char is not None:
            match self.state.current_char:
                case char if char.isspace():
                    self.skip_whitespace()
                    continue

                case char if char.isdigit():
                    return Token(TokenType.INT, self.integer())

                case char if char.isalpha():
                    return Token(TokenType.ID, self.identifier())

                case '/':
                    if self.text[self.pos + 1] == '/':
                        self.advance()
                        self.advance()
                        return Token(TokenType.COMMENT, self.comment())

                case "'":
                    self.advance()
                    return Token(TokenType.STRING, self.string())

                case char if char in PUNCTUATION:
                    token = Token(TokenType.PUNCTUATION, self.state.current_char)
                    self.advance()
                    return token

                case '+':
                    self.advance()
                    return Token(TokenType.PLUS, '+')

                case '-':
                    self.advance()
                    return Token(TokenType.MINUS, '-')

                case '*':
                    self.advance()
                    return Token(TokenType.MUL, '*')

                case '<':
                    self.advance()
                    return Token(TokenType.GREATER_THAN, '<')

                case '>':
                    self.advance()
                    return Token(TokenType.LESSER_THAN, '>')

                case '&':
                    self.advance()
                    return Token(TokenType.AMPERSAND_OPERATOR, '&')

                case '.':
                    self.advance()
                    return Token(TokenType.DOT_OPERATOR, '.')

                case '@':
                    self.advance()
                    return Token(TokenType.AT_OPERATOR, '@')

                case ';':
                    self.advance()
                    return Token(TokenType.SEMICOLON, ';')

                case '=':
                    self.advance()
                    return Token(TokenType.EQUAL, '=')

                case '~':
                    self.advance()
                    return Token(TokenType.CURL, '~')

                case '[':
                    self.advance()
                    return Token(TokenType.SQUARE_OPEN_BRACKET, '[')

                case ']':
                    self.advance()
                    return Token(TokenType.SQUARE_CLOSE_BRACKET, ']')

                case '$':
                    self.advance()
                    return Token(TokenType.DOLLAR, '$')

                case '!':
                    self.advance()
                    return Token(TokenType.EXCLAMATION_MARK, '!')

                case '#':
                    self.advance()
                    return Token(TokenType.HASH_TAG, '#')

                case '%':
                    self.advance()
                    return Token(TokenType.MODULUS, '%')

                case '^':
                    self.advance()
                    return Token(TokenType.CARROT, '^')

                case '{':
                    self.advance()
                    return Token(TokenType.CURLY_OPEN_BRACKET, '{')

                case '}':
                    self.advance()
                    return Token(TokenType.CURLY_CLOSE_BRACKET, '}')

                case '`':
                    self.advance()
                    return Token(TokenType.BACK_TICK, '`')

                case '"':
                    self.advance()
                    return Token(TokenType.DOUBLE_QUOTE, '"')

                case '?':
                    self.advance()
                    return Token(TokenType.QUESTION_MARK, '?')

                case '|':
                    self.advance()
                    return Token(TokenType.OR_OPERATOR, '|')

            self.error()

        return Token(TokenType.EOF, None)


class Screener:
    def __init__(self,tokens):
        self.text = None
        self.tokens=tokens

    def merge_tokens(self ):
        tokens=self.tokens

        for i in range(len(tokens)):

            if i < len(tokens) and tokens[i].type == TokenType.MINUS and tokens[i + 1].type == TokenType.LESSER_THAN:
                tokens[i].value = '->'
                tokens[i].type = TokenType.TERNARY_OPERATOR
                tokens.pop(i + 1)

            if i < len(tokens) and tokens[i].type == TokenType.GREATER_THAN and tokens[i + 1].type == TokenType.EQUAL:
                tokens[i].value = '>='
                tokens[i].type = TokenType.GREATER_THAN_OR_EQUAL
                tokens.pop(i + 1)

            if i < len(tokens) and tokens[i].type == TokenType.LESSER_THAN and tokens[i + 1].type == TokenType.EQUAL:
                tokens[i].value = '<='
                tokens[i].type = TokenType.LESSER_THAN_OR_EQUAL
                tokens.pop(i + 1)

            if i < len(tokens) and tokens[i].type == TokenType.MUL and tokens[i + 1].type == TokenType.MUL:
                tokens[i].value = '**'
                tokens[i].type = TokenType.POWER
                tokens.pop(i + 1)



        self.tokens=tokens

    def remove_comments(self):
        tokens = self.tokens
        tokens_to_be_Poped=[]
        for (i , token) in enumerate(tokens):
            if tokens[i].type == TokenType.COMMENT:
                tokens_to_be_Poped.append(i)
        for i in tokens_to_be_Poped:
            tokens.pop(i)

        self.tokens = tokens

    def screen_reserved_keywords(self):
        tokens=self.tokens
        for i in range(len(tokens)):
            if tokens[i].value in RESERVED_KEYWORDS:
                tokens[i].type=TokenType.RESERVED_KEYWORD
        self.tokens=tokens

    def screen(self):
        self.merge_tokens()
        self.remove_comments()
        self.screen_reserved_keywords()
        return self.tokens