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
    return (currentToken.type == type and currentToken.value == value)


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
        #tree pop function call?
        read_NT()
        while ((is_current_token="KEYWORD") & (is_current_token_type="L_PAREN")):
            procVB()
            #treesToPop++
        if (treesToPop):
        #I LEFT A CHUNK
    pass

def procEW():
    #T ’where’ DR
    print("procEW")
    procT()
    if(is_current_token("KEYWORD","where")):
        read_NT()
        proc_DR()
        buildNAryASTNode()#IDK WHAT TO PASS
    pass

def procT():
    print("procT")
    procTA()
    #extra readToken() in procTA()
    #int treesToPop = 0;
    while (is_current_token="OPERATOR",","):
        readNT()
        procTA()

        #treesToPop++;
        #if (treesToPop > 0)
        buildNAryASTNode()#IDK WHAT TO PASS

    pass

def procTA():

    pass

def procTC():
    print("ProcTC")
    procB()
    if (is_current_token="OPERATOR","->"):
        readNT()
        procTC()

        if (!is_current_token(OPERATOR, "|")):
            print("TC: '|' expected\n")
        
        readNT()
        procTC()

        buildNAryASTNode(ASTNodeType_CONDITIONAL, 3)

def proc_B():
    print("procB")

    proc_BT()
    # extra read_NT in proc_BT()
    while is_current_token(RESERVED, "or"):
        read_NT()
        proc_BT()
        build_n_ary_ast_node(ASTNodeType_OR, 2)

def proc_BT():
    print("procBT")

    proc_BS()
    # extra read_NT in proc_BS()
    while is_current_token(OPERATOR, "&"):
        read_NT()
        proc_BS()
        # extra read_NT in proc_BS()
        build_n_ary_ast_node(ASTNodeType_AND, 2)

def procBP():
    print("procBP")

    proc_A()
    # Bp -> A('gr' | '>' ) A => 'gr'
    if (is_current_token(RESERVED, "gr") || is_current_token(OPERATOR, ">")):
        read_NT()
        procA()
        build_n_ary_ast_node(ASTNodeType_GR, 2)

    #Bp -> A ('ge' | '>=') A => 'ge'
    else if (is_current_token(RESERVED, "ge") || is_current_token(OPERATOR, ">=")):
        readNT()
        procA()
        # extra readNT in procA()
        build_n_ary_ast_node(ASTNodeType_GE, 2)

    else if (is_current_token(RESERVED, "ls") || (is_current_token(OPERATOR, "<")):
        readNT()
        procA()
        # extra readNT in procA()
        build_n_ary_ast_node(ASTNodeType_LS, 2)

    else if (is_current_token(RESERVED, "le") || (is_current_token(OPERATOR, "<=")):
        readNT()
        procA()
        # extra readNT in procA()
        build_n_ary_ast_node(ASTNodeType_LE, 2)

    else if (is_current_token(RESERVED, "eq")):
        readNT()
        procA()
        # extra readNT in procA()
        build_n_ary_ast_node(ASTNodeType_EQ, 2)

    else if (is_current_token(RESERVED, "ne")):
        readNT()
        procA()
        # extra readNT in procA()
        build_n_ary_ast_node(ASTNodeType_NE, 2)
    pass

def procBS():
    print("procBS")

    if (is_current_token(RESERVED, "not")):
        readNT()
        procBP()
        # extra readNT in procA()
        build_n_ary_ast_node(ASTNodeType_NOT, 1)

    else:
        ProcBP()
        #Bs -> Bp
        #extra readNT in procBP()

    pass

def procAF():
    print("procAF")
    if (is_current_token(OPERATOR, "**")):
        readNT()
        procAF()
        # extra readNT in procA()
        build_n_ary_ast_node(ASTNodeType_EXP, 2)
    pass

def procAT():
    print("procAT")
    procAF()
    #At -> Af;
    #extra readNT in procAF()
    bool mult = True
    while (is_current_token(OPERATOR, "*") || is_current_token(OPERATOR, "/")):
        #if (strcmp(currentToken.value, "*") == 0)
         #   mult = true;
        #else if (strcmp(currentToken.value, "/") == 0)
         #   mult = false;
        #readNT();
        #procAF();
        #extra readNT in procAF()
        #if (mult) // At -> At '*' Af => '*'
        #   buildNAryASTNode(ASTNodeType_MULT, 2);
        #else // At -> At '/' Af => '/'
        #   buildNAryASTNode(ASTNodeType_DIV, 2);


         #CURRENT TOKEN????

    pass

def procA():
    print("procA")

    if (is_current_token(OPERATOR, "+")):
        readNT()
        procAT()
        # extra readNT in procAT()

    else if (is_current_token(OPERATOR, "-")):
        #A -> '-' At => 'neg'
        readNT()
        procAT()
        # extra readNT in procA()
        build_n_ary_ast_node(ASTNodeType_NEG, 1)

    bool plus=True
    while (is_current_token(OPERATOR, "+") || is_current_token(OPERATOR, "-")):
        if #AGAIN the current token thing:
        #Left a bunch

    pass

def procAP():
    print("procAP")
    ProcR()
    while (is_current_token(OPERATOR, "@")):
        readNT()
        if(!is_current_token(IDENTIFIER)):
           print("AP: expected Identifier")
        readNT()
        procR()
        # extra readNT in procR()
        build_n_ary_ast_node(ASTNodeType_AT, 3)

    pass

def procRN():
    print("procRN")
    if (is_current_token(IDENTIFIER) || is_current_token(INTEGER) || is_current_token(STRING)):
    #R -> '<IDENTIFIER>', R -> '<INTEGER>', R-> '<STRING>'
    #No need to do anything, as these are already processed in procR()
    
    else if (is_current_token(RESERVED, "True")):
    #create_terminal_ast_node?
        readNt()

    else if (is_current_token(RESERVED, "False")):
    #create_terminal_ast_node?
        readNt()

    else if (is_current_token(RESERVED, "nil")):
    #create_terminal_ast_node?
        readNt()

    else if (is_current_token_type(L_PAREN)):
        readNT()
        procE()
        if(!is_current_token_type(R_PAREN)):
           #Replace with appropriate error handling
           print("RN: ')' expected")
        #printf("procRN: (E) done");
        #readNT();

    else if (is_current_token_type(RESERVED, "dummy")):
    #create_terminal_ast_node?
        readNt()

    pass

def procR():
    print("procR")
    while (is_current_token(IDENTIFIER) || 
        is_current_token(INTEGER) || 
        is_current_token(STRING) || 
        is_current_token(RESERVED, "True") || 
        is_current_token(RESERVED, "False") || 
        is_current_token(RESERVED, "nil") || 
        is_current_token(RESERVED, "dummy") || 
        is_current_token(L_PAREN)):

        procRN()
        build_n_ary_ast_node(ASTNodeType_GAMMA, 2)
        #print("Build gamma done")
        readNT()
    
    pass

def procDR():
    print("procDR")
    
    if (is_current_token(RESERVED, "rec")):
        readNT()
        procDB()
        build_n_ary_ast_node(ASTNodeType_REC, 1)

    else:
        procDB()
    
    pass

def procDA():
    print("procDA")
    procDR()
    #some pop thing
    while (is_current_token(RESERVED, "and")):
        readNT()
        procDR()
        #pop thing
    
    if (treesToPOP > 0)
        build_n_ary_ast_node(ASTNodeType_SIMULTDEF, treesToPop + 1)
    pass

def procD():
    print("procD")
    procDA()
    if (is_current_token(RESERVED, "within")):
        readNT()
        procD()
        build_n_ary_ast_node(ASTNodeType_WITHIN, 2)

    pass

def procDB():
    print("procDB")
    
    if (is_current_token_type(L_PAREN)):
        readNT()
        procD()
        readNT()

        if(!is_current_token_type(R_PAREN)):
           print("Error handling")
        
        readNT(0)
    
    else if (is_current_token_type(IDENTIFIER)):
        readNT()

#HAVE MOREEEEEEEEEEEEE
        build_n_ary_ast_node(ASTNodeType_WITHIN, 2)

    pass

def procVB():
    print("procVB")
    
    if (is_current_token_type(IDENTIFIER)):
        #Vb -> '<IDENTIFIER>'
        readNT()

    else if (is_current_token_type(L_PAREN)):
        readNT()
        if (is_current_token_type(R_PAREN)):
        #Vb -> '(' ')' => '()'
        create_terminal_ast_node(ASTNodeType_PAREN, "", currentToken.sourceLineNumber);
            readNT()

    else:
        procVL()
        if (!is_current_token_type(R_PAREN))
            print("VB: ')' expected")
            readNT()
    pass

def procVL():
    print("procVL")

    if (!is_current_token_type(IDENTIFIER)):
        print("VL: Identifier expected")

    else:
        readNT()
        int treesToPop=0
        while (is_current_token(OPERATOR, ",")):
            readNT()
            if (!is_current_token_type(IDENTIFIER)):
                print("VL: Identifier expected")
                readNT()
                treesToPop += 1
            
        if (treesToPop>0):
            build_n_ary_ast_node(ASTNodeType_COMMA, treesToPop + 1)
        
    pass