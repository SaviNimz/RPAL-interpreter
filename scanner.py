import re

# Define regular expressions for each token type with updated keywords
patterns = {
    'KEYWORD': r'(let|ls|le|eq|ne|true|false|nil|dummy|where|in|fn|and|rec|within|aug|not|or|gr|ge)',
    'IDENTIFIER': r'[a-zA-Z_][a-zA-Z0-9_]*',
    'INTEGER': r'\d+',
    'OPERATOR': r'[\+\-\*/=<>]+',
    'STRING': r'\".*?\"',
    'DELETE': r'delete',
    'PUNCTUATION': r'[,;()\[\]\{\}]',
    'END': r'\$'
}

combined_pattern = '|'.join(f'(?P<{token}>{pattern})' for token, pattern in patterns.items())

def preprocess(text):
    # Remove everything after '//'
    return re.sub(r'//.*', '', text)

def scan(text):
    tokens = []
    for match in re.finditer(combined_pattern, text):
        for token, pattern in patterns.items():
            if match.group(token):
                tokens.append((token, match.group(token)))
                break
    return tokens

def tokenize_file(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
        code = preprocess(code)
        return scan(code)



