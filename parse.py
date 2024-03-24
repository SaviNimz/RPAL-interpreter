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


stack = Stack(100)  # Initialize the stack with a given capacity
currentToken = None  # Define currentToken

def push(node):
    global stack
    stack.top += 1
    stack.arr[stack.top] = node

def pop():
    global stack
    node = stack.arr[stack.top]
    stack.top -= 1
    return node

def is_empty():
    global stack
    return stack.top == -1

def print_ast(ast_node, depth):
    # Pre-order traversal
    print("-" * depth, ast_node.type, ast_node.value if ast_node.value is not None else "")
    if ast_node.child is not None:
        print_ast(ast_node.child, depth + 1)
    if ast_node.sibling is not None:
        print_ast(ast_node.sibling, depth)

def print_stack():
    global stack
    print("\nStack:", stack.top)
    for i in range(stack.top + 1):
        print_ast(stack.arr[i], 0)
        print()

def build_n_ary_ast_node(type, ariness):
    node = ASTNode(type)
    node.child = None
    node.sibling = None
    node.sourceLineNumber = -1

    while ariness > 0:
        child = pop()  # Assuming there's a function pop() to retrieve child nodes
        if node.child is not None:
            child.sibling = node.child
        node.child = child
        node.sourceLineNumber = child.sourceLineNumber

        ariness -= 1

    push(node)  # Assuming there's a function push() to push the node onto some stack

    return node

def create_terminal_ast_node(type, value, sourceLineNumber):
    node = ASTNode(type, value, sourceLineNumber)
    push(node)
    return node

def is_current_token_type(type):
    global currentToken
    return currentToken.type == type

def is_current_token(type, value):
    global currentToken
    return currentToken.type == type and currentToken.value == value


#following function can have errors check it
def read_NT():
    global currentToken, tokens, token_index

    while True:
        _token = tokens[token_index]
        token_index += 1
        currentToken.sourceLineNumber = _token.sourceLineNumber
        currentToken.value = _token.value

        if _token.type == TokenType.RESERVED:
            currentToken.type = ASTNodeType.LET
        elif _token.type == TokenType.IDENTIFIER:
            currentToken.type = ASTNodeType.IDENTIFIER
        elif _token.type == TokenType.STRING:
            currentToken.type = ASTNodeType.STRING
        elif _token.type == TokenType.INTEGER:
            currentToken.type = ASTNodeType.INTEGER
        elif _token.type == TokenType.OPERATOR:
            currentToken.type = ASTNodeType.OPERATOR
        elif _token.type == TokenType.L_PAREN:
            if _token.value == "(":
                currentToken.type = ASTNodeType.PAREN
        elif _token.type == TokenType.END_TOKEN:
            currentToken.value = None
            currentToken.type = ASTNodeType.DUMMY

        if not is_current_token_type(TokenType.DELETE):
            break

    if currentToken.value is not None:
        if currentToken.type == ASTNodeType.IDENTIFIER:
            node = create_terminal_ast_node(ASTNodeType.IDENTIFIER, currentToken.value, currentToken.sourceLineNumber)
        elif currentToken.type == ASTNodeType.INTEGER:
            node = create_terminal_ast_node(ASTNodeType.INTEGER, currentToken.value, currentToken.sourceLineNumber)
        elif currentToken.type == ASTNodeType.STRING:
            node = create_terminal_ast_node(ASTNodeType.STRING, currentToken.value, currentToken.sourceLineNumber)



