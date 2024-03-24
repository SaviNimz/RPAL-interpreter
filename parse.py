from scanner import tokenize_file
from enum import Enum,auto


file_path = 'input.rpal'
tokens = tokenize_file(file_path)


class ASTNodeType(Enum):
    LET = 1
    LAMBDA = 2
    WHERE = 3
    TAU = 4
    AUG = 5
    CONDITIONAL = 6
    OR = 7
    AND = 8
    NOT = 9
    GR = 10
    GE = 11
    LS = 12
    LE = 13
    EQ = 14
    NE = 15
    NEG = 16
    PLUS = 17
    MINUS = 18
    MULT = 19
    DIV = 20
    EXP = 21
    AT = 22
    GAMMA = 23
    TRUE = 24
    FALSE = 25
    NIL = 26
    DUMMY = 27
    WITHIN = 28
    SIMULTDEF = 29
    REC = 30
    COMMA = 31
    EQUAL = 32
    FCNFORM = 33
    PAREN = 34
    IDENTIFIER = 35
    INTEGER = 36
    STRING = 37
class TokenType(Enum):
    RESERVED = auto()
    OPERATOR = auto()
    IDENTIFIER = auto()
    L_PAREN = auto()
    INTEGER = auto()
    STRING = auto()
    R_PAREN = auto()
    DELETE = auto()
    END_TOKEN = auto()


    
class Token:
    def __init__(self, type, value, sourceLineNumber):
        self.type = type
        self.value = value
        self.sourceLineNumber = sourceLineNumber

# we can use objects of this class to create abstract syntax tree node objects 
class ASTNode:
    def __init__(self, type, value, sourceLineNumber):
        self.type = type
        self.value = value
        self.sourceLineNumber = sourceLineNumber
        self.child = None
        self.sibling = None

# we can use the following class to create stacks 
        
class Stack:
    def __init__(self):
        self.arr = []
    
    def push(self, node):
        self.arr.append(node)
    
    def pop(self):
        if self.arr:
            return self.arr.pop()
        return None
    
    def is_empty(self):
        return len(self.arr) == 0

# Global variables
stack = Stack()
current_token = Token(None, None, None)
token_index = 0





def is_current_token_type(type):
    return current_token.type == type

def is_current_token(type, value):
    return current_token.type == type and current_token.value == value