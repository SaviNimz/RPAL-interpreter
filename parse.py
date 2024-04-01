from scanner import tokenize_file
from enum import Enum,auto
from collections import deque



file_path = 'input.rpal'

# here we have the tokens that are tokenized from the input file 

tokens = tokenize_file(file_path)
token_index = 0

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

class ASTNodeType(Enum):
    ASTNodeType_LET = auto()
    ASTNodeType_LAMBDA = auto()
    ASTNodeType_WHERE = auto()
    ASTNodeType_TAU = auto()
    ASTNodeType_AUG = auto()
    ASTNodeType_CONDITIONAL = auto()
    ASTNodeType_OR = auto()
    ASTNodeType_AND = auto()
    ASTNodeType_NOT = auto()
    ASTNodeType_GR = auto()
    ASTNodeType_GE = auto()
    ASTNodeType_LS = auto()
    ASTNodeType_LE = auto()
    ASTNodeType_EQ = auto()
    ASTNodeType_NE = auto()
    ASTNodeType_NEG = auto()
    ASTNodeType_PLUS = auto()
    ASTNodeType_MINUS = auto()
    ASTNodeType_MULT = auto()
    ASTNodeType_DIV = auto()
    ASTNodeType_EXP = auto()
    ASTNodeType_AT = auto()
    ASTNodeType_GAMMA = auto()
    ASTNodeType_TRUE = auto()
    ASTNodeType_FALSE = auto()
    ASTNodeType_NIL = auto()
    ASTNodeType_DUMMY = auto()
    ASTNodeType_WITHIN = auto()
    ASTNodeType_SIMULTDEF = auto()
    ASTNodeType_REC = auto()
    ASTNodeType_COMMA = auto()
    ASTNodeType_EQUAL = auto()
    ASTNodeType_FCNFORM = auto()
    ASTNodeType_PAREN = auto()
    ASTNodeType_IDENTIFIER = auto()
    ASTNodeType_INTEGER = auto()
    ASTNodeType_STRING = auto()

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

#initialize the global stack
    
stack = Stack()  

# we use this token to loop through the array of tokens and this serves as a global pointer 
currentToken = tokens[0] 

def push(node):
    global stack
    stack.push(node)

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



# We use the following function to build the AST using stack based approach
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


# this function is responsible for advancing through token stream
def read_NT():

    global currentToken, tokens, token_index

    _token = tokens[token_index]
    token_index += 1
    currentToken.sourceLineNumber = _token.sourceLineNumber
    currentToken.value = _token.value

    if _token.type == "KEYWORD":
        currentToken.type = "RESERVED"
    elif _token.type == "IDENTIFIER":
        currentToken.type = "IDENTIFIER"
    elif _token.type == "INTEGER":
        currentToken.type = "INTEGER"
    elif _token.type == "OPERATOR":
        currentToken.type = "OPERATOR"
    elif _token.type == "STRING":
        currentToken.type = "STRING"
    elif _token.type == "PUNCTUATION":
        currentToken.type = "PUNCTUATION"

    if currentToken.value is not None:
        if currentToken.type == "IDENTIFIER":
            node = create_terminal_ast_node(ASTNodeType.ASTNodeType_IDENTIFIER, currentToken.value, currentToken.sourceLineNumber)
        elif currentToken.type == "INTEGER":
            node = create_terminal_ast_node(ASTNodeType.ASTNodeType_INTEGER, currentToken.value, currentToken.sourceLineNumber)
        elif currentToken.type == "STRING":
            node = create_terminal_ast_node(ASTNodeType.ASTNodeType_STRING, currentToken.value, currentToken.sourceLineNumber)

    # update the current token
    currentToken = tokens[token_index]

