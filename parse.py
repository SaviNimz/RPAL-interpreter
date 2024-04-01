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
    print(stack.arr[0].type)
    node = stack.pop()
    return node

def is_empty():
    global stack
    return stack.top == -1

def print_ast(ast_node, depth):
    if ast_node is None:
        return
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

    print("heyy someone called me !!")
    node = ASTNode(type,None,-1)
    # node.child = None
    # node.sibling = None


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
    print(currentToken.type,currentToken.value)
    return (currentToken.type == type and currentToken.value == value)

# this function is responsible for advancing through token stream
def read_NT():

    print('hi')
    global currentToken, tokens, token_index

    _token = tokens[token_index]

    print('up')
    token_index += 1
    currentToken.sourceLineNumber = _token.sourceLineNumber
    currentToken.value = _token.value

    if _token.type == "KEYWORD":
        currentToken.type = "KEYWORD"
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

def procE():
    print("procE")
    if (is_current_token("KEYWORD","let")):
        #read the non-terminal function
        read_NT()
        procD()
        if not (is_current_token("KEYWORD","in")):
            print("E: 'in' expected")
            exit(0)
        #read the non-terminal function
        read_NT()
        procE()
        build_n_ary_ast_node(ASTNodeType.ASTNodeType_LET, 2)

    elif (is_current_token("KEYWORD","fn")):
        treesToPop = 0
        read_NT()
        # putting punctuation here is a problem
        while (is_current_token_type("KEYWORD") and is_current_token_type("L_PAREN")):
            procVB()
            treesToPop += 1
            if (treesToPop == 0):
                print("E: atleast one 'Vb' expected" )

            if not (is_current_token("OPERATOR", ".")):
                print("E: '.' expected ")

            read_NT()
            procE()
            build_n_ary_ast_node(ASTNodeType.ASTNodeType_LAMBDA,treesToPop+1)
    else:
        procEW()

def procEW():
    #T ’where’ DR
    print("procEW")
    procT()
    if(is_current_token("KEYWORD","where")):
        read_NT()
        procDR()
        build_n_ary_ast_node(ASTNodeType.ASTNodeType_WHERE,2)

def procT():
    print("procT")
    procTA()
    #extra readToken() in procTA()
    treesToPop = 0
    while (is_current_token("OPERATOR",",")):
        read_NT()
        procTA()

        treesToPop += treesToPop
        if (treesToPop > 0):

            build_n_ary_ast_node(ASTNodeType.ASTNodeType_TAU,treesToPop+1)

def procTA():
    print("procTA")
    procTC()
    while (is_current_token("KEYWORD", "aug")):
        read_NT()
        procTC()
        build_n_ary_ast_node(ASTNodeType.ASTNodeType_AUG,2) 

def procTC():
    print("ProcTC")
    procB()
    if(is_current_token("OPERATOR","->")):
        read_NT()
        procTC()

        if not (is_current_token("OPERATOR", "|")):
            print("TC: '|' expected\n")
        
        read_NT()
        procTC()

        build_n_ary_ast_node(ASTNodeType.ASTNodeType_CONDITIONAL, 3)

def procB():
    print("procB")
    procBT()
    # extra read_NT in proc_BT()
    while (is_current_token("KEYWORD", "or")):
        read_NT()
        procBT()
        build_n_ary_ast_node(ASTNodeType.ASTNodeType_OR, 2)

def procBT():
    print("procBT")
    procBS()
    # extra read_NT in proc_BS()
    while is_current_token("OPERATOR", "&"):
        read_NT()
        procBS()
        # extra read_NT in proc_BS()
        build_n_ary_ast_node(ASTNodeType.ASTNodeType_AND, 2)

def procBP():
    print("procBP")
    procA()
    # Bp -> A('gr' | '>' ) A => 'gr'
    if ((is_current_token("KEYWORD", "gr") or is_current_token("OPERATOR", ">"))):
        read_NT()
        procA()
        build_n_ary_ast_node(ASTNodeType.ASTNodeType_GR, 2)

    #Bp -> A ('ge' | '>=') A => 'ge'
    elif ((is_current_token("KEYWORD", "ge") or is_current_token("OPERATOR", ">="))):
        read_NT()
        procA()
        # extra readNT in procA()
        build_n_ary_ast_node(ASTNodeType.ASTNodeType_GE, 2)

    elif ((is_current_token("KEYWORD", "ls")) or (is_current_token("OPERATOR", "<"))):
        read_NT()
        procA()
        # extra readNT in procA()
        build_n_ary_ast_node(ASTNodeType.ASTNodeType_LS, 2)

    elif ((is_current_token("KEYWORD", "le")) or (is_current_token("OPERATOR", "<="))):
        read_NT()
        procA()
        # extra readNT in procA()
        build_n_ary_ast_node(ASTNodeType.ASTNodeType_LE, 2)

    elif (is_current_token("KEYWORD", "eq")):
        read_NT()
        procA()
        # extra readNT in procA()
        build_n_ary_ast_node(ASTNodeType.ASTNodeType_EQ, 2)

    elif (is_current_token("KEYWORD", "ne")):
        read_NT()
        procA()
        # extra readNT in procA()
        build_n_ary_ast_node(ASTNodeType.ASTNodeType_NE, 2)

def procBS():
    print("procBS")
    if (is_current_token("RESERVED", "not")):
        read_NT()
        procBP()
        # extra readNT in procA()
        build_n_ary_ast_node(ASTNodeType.ASTNodeType_NOT, 1)
    else:
        procBP()

def procAF():
    print("procAF")
    if (is_current_token("OPERATOR", "**")):
        read_NT()
        procAF()
        build_n_ary_ast_node(ASTNodeType.ASTNodeType_EXP, 2)

def procAT():
    print("procAT")
    procAF()
    #At -> Af;
    #extra readNT in procAF()
    mult = True
    while ((is_current_token("OPERATOR", "*")) or (is_current_token("OPERATOR", "/"))):

        if (currentToken.value == "*"):
            mult = True
        elif(currentToken.value == "/"):
            mult = False
        read_NT()
        procAF()

        if(mult):
            build_n_ary_ast_node(ASTNodeType.ASTNodeType_MULT, 2)
        else:
            build_n_ary_ast_node(ASTNodeType.ASTNodeType_DIV, 2)

def procA():
    print("procA")

    if (is_current_token("OPERATOR", "+")):
        read_NT()
        procAT()
        # extra readNT in procAT()

    elif (is_current_token("OPERATOR", "-")):
        #A -> '-' At => 'neg'
        read_NT()
        procAT()
        # extra readNT in procA()
        build_n_ary_ast_node(ASTNodeType.ASTNodeType_NEG, 1)

    plus=True

    while (is_current_token("OPERATOR", "+") or is_current_token("OPERATOR", "-")):
        if(currentToken.value == "+"):
            plus = True
        elif(currentToken.value == "-"):
            plus = False

        read_NT()
        procAT()

        if(plus):
            build_n_ary_ast_node(ASTNodeType.ASTNodeType_PLUS, 2)
        else:
            build_n_ary_ast_node(ASTNodeType.ASTNodeType_MINUS, 2)

def procAP():
    print("procAP")
    procR()
    while (is_current_token("OPERATOR", "@")):
        read_NT()
        if(not is_current_token("IDENTIFIER")):
           print("AP: expected Identifier")
        read_NT()

        procR()

        build_n_ary_ast_node(ASTNodeType.ASTNodeType_AT, 3)

def procRN():
    print("procRN")
    #if (is_current_token("IDENTIFIER") or is_current_token("INTEGER") or is_current_token("STRING")):
    #R -> '<IDENTIFIER>', R -> '<INTEGER>', R-> '<STRING>'
    #No need to do anything, as these are already processed in procR()
    
    if (is_current_token("KEYWORD", "True")):
        create_terminal_ast_node(ASTNodeType.ASTNodeType_TRUE,"true",currentToken.sourceLineNumber)
        read_NT()

    elif (is_current_token("KEYWORD", "False")):
        create_terminal_ast_node(ASTNodeType.ASTNodeType_FALSE,"false",currentToken.sourceLineNumber)
        read_NT()

    elif (is_current_token("KEYWORD", "nil")):
        create_terminal_ast_node(ASTNodeType.ASTNodeType_NIL,"nil",currentToken.sourceLineNumber)
        read_NT()

    elif (is_current_token_type("L_PAREN")):
        read_NT()
        procE()

        if not (is_current_token_type("R_PAREN")):
           #Replace with appropriate error handling
           print("RN: ')' expected")

    elif (is_current_token_type("KEYWORD" "dummy")):
        build_n_ary_ast_node(ASTNodeType.ASTNodeType_DUMMY, "dummy", currentToken.sourceLineNumber)
        read_NT()
    pass

def procR():
    print("procR")
    while (is_current_token("IDENTIFIER") or 
            is_current_token("INTEGER") or 
            is_current_token("STRING") or 
            is_current_token("KEYWORD", "True") or 
            is_current_token("KEYWORD", "False") or 
            is_current_token("KEYWORD", "nil") or 
            is_current_token("KEYWORD", "dummy") or 
            is_current_token("L_PAREN")):

        procRN()
        build_n_ary_ast_node(ASTNodeType.ASTNodeType_GAMMA, 2)
        read_NT()

def procDR():
    print("procDR")
    
    if (is_current_token("KEYWORD", "rec")):
        read_NT()
        procDB()
        build_n_ary_ast_node(ASTNodeType.ASTNodeType_REC, 1)

    else:
        procDB()

def procDA():
    print("procDA")
    procDR()

    treesToPop = 0
    
    while (is_current_token("KEYWORD", "and")):
        read_NT()
        procDR()
        #pop thing
    
    if (treesToPop > 0):
        build_n_ary_ast_node(ASTNodeType.ASTNodeType_SIMULTDEF, treesToPop + 1)

def procD():
    print("procD")
    procDA()
    if (is_current_token("KEYWORD", "within")):
        read_NT()
        procD()
        build_n_ary_ast_node(ASTNodeType.ASTNodeType_WITHIN, 2)

def procDB():
    print("procDB")
    
    if (is_current_token_type("L_PAREN")):
        read_NT()
        procD()
        read_NT()

        if(not is_current_token_type("R_PAREN")):
           print("Error handling")
        
        read_NT()
    
    elif (is_current_token_type("IDENTIFIER")):
        read_NT()
        if (is_current_token("OPERATOR", ",")):
            read_NT()
            procVB()

            if not (is_current_token("OPERATOR","=")):
                print("DB: = expected.")
            
            build_n_ary_ast_node(ASTNodeType.ASTNodeType_COMMA,2)
            read_NT()
            procE()
            build_n_ary_ast_node(ASTNodeType.ASTNodeType_EQUAL,2)

        else:
            if(is_current_token("OPERATOR", "=")):

                read_NT()
                procE()
                build_n_ary_ast_node(ASTNodeType.ASTNodeType_EQUAL,2)
            
            else:
                treesToPop = 0

                while(is_current_token_type("IDENTIFIER") or is_current_token_type("L_PAREN")):
                    procVB()
                    treesToPop += 1

                if(treesToPop == 0):
                    print("E: at least one 'Vb' expected")
                
                read_NT()
                procE()

                build_n_ary_ast_node(ASTNodeType.ASTNodeType_FCNFORM,treesToPop+2)

def procVB():
    print("procVB")
    
    if (is_current_token_type("IDENTIFIER")):
        #Vb -> '<IDENTIFIER>'
        read_NT()

    elif (is_current_token_type("L_PAREN")):
        read_NT()
        if (is_current_token_type("R_PAREN")):
        #Vb -> '(' ')' => '()'
            create_terminal_ast_node(ASTNodeType.ASTNodeType_PAREN, "", currentToken.sourceLineNumber)
            read_NT()

    else:
        procVL()
        if (not is_current_token_type("R_PAREN")):
            print("VB: ')' expected")
            read_NT()

def procVL():
    print("procVL")

    if not  (is_current_token_type("IDENTIFIER")):
        print("VL: Identifier expected")

    else:
        read_NT()
        treesToPop=0
        while (is_current_token("OPERATOR", ",")):
            read_NT()
            if (not is_current_token_type("IDENTIFIER")):
                print("VL: Identifier expected")
                read_NT()
                treesToPop += 1
            
        if (treesToPop>0):
            build_n_ary_ast_node(ASTNodeType.ASTNodeType_COMMA, treesToPop + 1)


def startParse():

    read_NT()
    procE()

    if(currentToken.value != None):
        print(currentToken.value)

def buildAST():

    startParse()

    return pop()


root = buildAST()

print_ast(root,0)
