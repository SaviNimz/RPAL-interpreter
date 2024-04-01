import re

class Token:
    def __init__(self, type, value, sourceLineNumber):
        self.type = type
        self.value = value
        self.sourceLineNumber = sourceLineNumber

patterns = {
    'KEYWORD': r'(let|ls|le|eq|ne|true|false|nil|dummy|where|in|fn|and|rec|within|aug|not|or|gr|ge)',
    'IDENTIFIER': r'[a-zA-Z_][a-zA-Z0-9_]*',
    'INTEGER': r'\d+',
    'OPERATOR': r'[\+\-\*/=<>|\.]+',
    'STRING': r'\".*?\"',
    'DELETE': r'delete',
    'PUNCTUATION': r'[,;\[\]\{\}]',
    'END': r'\$',
    'L_PAREN': r'\(',
    'R_PAREN': r'\)'
}

combined_pattern = '|'.join(f'(?P<{token}>{pattern})' for token, pattern in patterns.items())

def preprocess(text):
    return re.sub(r'//.*', '', text)

def tokenize_file(file_path):
    tokens = []
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            line = preprocess(line)
            for match in re.finditer(combined_pattern, line):
                for token, pattern in patterns.items():
                    if match.group(token):
                        tokens.append(Token(token, match.group(token), line_number))
                        break
    return tokens

t = tokenize_file('input.rpal')
