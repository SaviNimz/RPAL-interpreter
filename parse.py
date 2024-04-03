import Tokenizer
from Tokenizer import Screener

#Defining a class for ASTNode
class ASTNode:
    def __init__(self, type):
        self.type = type
        self.value = None
        self.sourceLineNumber = -1
        self.child = None
        self.sibling = None
        self.indentation = 0
    #Print tree
    def print_tree(self):
        print(self.type)

        if self.child:
            print(" child of " + str(self.type) + " is ",end=" ")
            self.child.print_tree()
        if self.sibling:
            print(" sibling of " + str(self.type) + " is " ,end=" ")

            self.sibling.print_tree()

    #Print tree to file
    def print_tree_to_file(self, file):

        for i in range(self.indentation):
            file.write(".")
        # if(self.type ==)
        file.write(str(self.type) + "\n")

        if self.child:

            self.child.indentation = self.indentation + 1
            self.child.print_tree_to_file(file)
        if self.sibling:
            self.sibling.indentation = self.indentation
            self.sibling.print_tree_to_file(file)

#Defining a class for Tree Node
class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []
        self.parent = None

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def print_tree(self):
        print(self.data)
        if self.children:
            for child in self.children:
                child.print_tree()

#Defining a class for AST Parser
class ASTParser:

    def __int__(self, tokens1):
        self.tokens = tokens1
        self.current_token = None
        self.index = 0

    def read(self):

        if self.current_token.type in [Tokenizer.TokenType.ID, Tokenizer.TokenType.INT,
                                       Tokenizer.TokenType.STRING] :

            terminalNode = ASTNode( "<"+str(self.current_token.type.value)+":"+  str(self.current_token.value)+">")
            stack.append(terminalNode)

        if self.current_token.value in  ['true', 'false', 'nil', 'dummy']:
            stack.append(ASTNode(self.current_token.value))

        print("reading : " + str(self.current_token.value))
        self.index += 1

        if (self.index < len(self.tokens)):
            self.current_token = self.tokens[self.index]

    def buildTree(self, token, ariness):
        global stack

        print("stack content before ")
        for node in stack:
            print(node.type)

        print("building tree")

        node = ASTNode(token)
        node.value = None
        node.sourceLineNumber = -1
        node.child = None
        node.sibling = None

        while ariness > 0:
            child = stack[-1]
            stack.pop()
            if node.child is not None:
                child.sibling = node.child
            node.child = child
            node.sourceLineNumber = child.sourceLineNumber
            ariness -= 1

        node.print_tree()

        stack.append(node)  
        print("stack content after")
        for node in stack:
            print(node.type)

    #Defining process E
    def processE(self):
        print('procE')
        match self.current_token.value:

            case 'let':
                self.read()
                self.processD()

                if self.current_token.value != 'in':
                    print("Error: in is expected")
                    return

                self.read()
                self.processE()
                print('E->let D in E')
                self.buildTree("let", 2)

            case 'fn':
                n = 0
                self.read()

                while self.current_token.type == Tokenizer.TokenType.ID or self.current_token.value == '(':
                    self.processVb()
                    n += 1

                if n == 0:
                    print("E: at least one 'Vb' expected\n")
                    return

                if self.current_token.value != '.':
                    print("Error: . is expected")
                    return

                self.read()
                self.processE()
                print('E->fn Vb . E')
                self.buildTree("lambda", n+1)

            case _:
                self.processEw()
                print('E->Ew')

    #Defining process Ew
    def processEw(self):
        print('procEw')
        self.processT()
        print('Ew->T')
        if self.current_token.value == 'where':
            self.read()
            self.processDr()
            print('Ew->T where Dr')
            self.buildTree("where", 2)

    #Defining process T  
    def processT(self):
        print('procT')
        self.processTa()
        n = 0
        while self.current_token.value == ',':
            self.read()
            self.processTa()
            n += 1
            print('T->Ta , Ta')
        if n > 0:
            self.buildTree("tau", n + 1)
        else:
            print('T->Ta')

    #Defining process Ta
    def processTa(self):
        print('procTa')
        self.processTc()
        print('Ta->Tc')
        while self.current_token.value == 'aug':
            self.read()
            self.processTc()
            print('Ta->Tc aug Tc')

            self.buildTree("aug", 2)

    #Defining process Tc
    def processTc(self):
        print('procTc')

        self.processB()
        print('Tc->B')
        if self.current_token.type == Tokenizer.TokenType.TERNARY_OPERATOR:
            self.read()
            self.processTc()

            if self.current_token.value != '|':
                print("Error: | is expected")
                return
            self.read()
            self.processTc()
            print('Tc->B -> Tc | Tc')
            self.buildTree("->", 3)

    #Defining process B
    def processB(self):
        print('procB')

        self.processBt()
        print('B->Bt')
        while self.current_token.value == 'or':
            self.read()
            self.processBt()
            print('B->B or B')
            self.buildTree("or", 2)

    #Defining process Bt
    def processBt(self):
        print('procBt')

        self.processBs()
        print('Bt->Bs')
        while self.current_token.value == '&':
            self.read()
            self.processBs()
            print('Bt->Bs & Bs')
            self.buildTree("&", 2)

    #Defining process Bs
    def processBs(self):
        print('procBs')

        if self.current_token.value == 'not':
            self.read()
            self.processBp()
            print('Bs->not Bp')
            self.buildTree("not", 1)
        else:
            self.processBp()
            print('Bs->Bp')

    #Defining process Bp
    def processBp(self):
        print('procBp')

        self.processA()
        print('Bp->A')
        print(self.current_token.value+"######")

        match self.current_token.value:
            case '>':
                self.read()
                self.processA()
                print('Bp->A gr A')
                self.buildTree("gr", 2)
            case 'gr':
                self.read()
                self.processA()
                print('Bp->A gr A')
                self.buildTree("gr", 2)

            case 'ge':
                self.read()
                self.processA()
                print('Bp->A ge A')
                self.buildTree("ge", 2)

            case '>=':
                self.read()
                self.processA()
                print('Bp->A ge A')
                self.buildTree("ge", 2)

            case '<':
                self.read()
                self.processA()
                print('Bp->A ls A')
                self.buildTree("ls", 2)

            case 'ls':
                self.read()
                self.processA()
                print('Bp->A ls A')
                self.buildTree("ls", 2)

            case '<=':
                self.read()
                self.processA()
                print('Bp->A le A')
                self.buildTree("le", 2)

            case 'le':
                self.read()
                self.processA()
                print('Bp->A le A')
                self.buildTree("le", 2)

            case 'eq':
                self.read()
                self.processA()
                print('Bp->A eq A')
                self.buildTree("eq", 2)

            case 'ne':
                self.read()
                self.processA()
                print('Bp->A ne A')
                self.buildTree("ne", 2)

            case _:
                return

    #Defining process A
    def processA(self):
        print('procA')

        if self.current_token.value == '+':
            self.read()
            self.processAt()
            print('A->+ At')

        elif self.current_token.value == '-':
            self.read()
            self.processAt()
            print('A->- At')
            self.buildTree("neg", 1)


        else:
            self.processAt()
            print('A->At')
        plus = '+'
        while self.current_token.value == '+' or self.current_token.value == '-':

            if self.current_token.value=='-':
                plus='-'

            self.read()
            self.processAt()
            print('A->A + / -At')
            print(self.current_token.value)
            self.buildTree(plus, 2)

    #Defining process At
    def processAt(self):
        print('procAt')

        self.processAf()
        print('At->Af')
        while self.current_token.value == '*' or self.current_token.value == '/':
            self.read()
            self.processAf()
            print('At->Af * Af')
            print("current token value " + self.current_token.value)
            self.buildTree(self.current_token.value, 2)

    #Defining process Af
    def processAf(self):
        print('procAf')

        self.processAp()
        print('Af->Ap')
        while self.current_token.value == '**':
            self.read()
            self.processAf()
            print('Af->Ap ** Af')
            self.buildTree("**", 2)

    #Defining process Ap
    def processAp(self):
        print('procAp')

        self.processR()
        print('Ap->R')
        while self.current_token.value == '@':
            self.read()
            self.processR()
            print('Ap->R @ R')
            self.buildTree("@", 2)

    #Defining process R
    def processR(self):
        print('procR')

        self.processRn()
        print('R->Rn')
        while (self.current_token.type in [Tokenizer.TokenType.ID, Tokenizer.TokenType.INT,
                                            Tokenizer.TokenType.STRING] or self.current_token.value in 
                                            ['true', 'false','nil', 'dummy',"("]):
            self.processRn()
            print('R->R Rn')
            self.buildTree("gamma", 2)

    #Defining process Rn
    def processRn(self):
        print("procRn")

        if self.current_token.type in [Tokenizer.TokenType.ID, Tokenizer.TokenType.INT,
                                       Tokenizer.TokenType.STRING]:

            print('Rn->' + str(self.current_token.value))

            self.read()

        elif self.current_token.value in ['true', 'false', 'nil', 'dummy']:
            print('Rn->' + self.current_token.value)
            self.read()
            print("self.current_token.value" , self.current_token.value)

        elif self.current_token.value == '(':
            self.read()
            self.processE()
            if self.current_token.value != ')':
                print("Error: ) is expected")
                return
            self.read()
            print('Rn->( E )')

    #Defining process D
    def processD(self):
        print('procD')

        self.processDa()
        print('D->Da')
        while self.current_token.value == 'within':
            self.read()
            self.processD()
            print('D->Da within D')
            self.buildTree("within", 2)

    #Defining process Da
    def processDa(self):
        print('procDa')

        self.processDr()
        print('Da->Dr')
        n = 0
        while self.current_token.value == 'and':
            n += 1
            self.read()
            self.processDa()
            print('Da->and Dr')
        if n > 0:
            self.buildTree("and", n + 1)

    #Defining process Dr
    def processDr(self):
        print('procDr')
        if self.current_token.value == 'rec':
            self.read()
            self.processDb()
            print('Dr->rec Db')
            self.buildTree("rec", 1)

        self.processDb()
        print('Dr->Db')

    #Defining process Db
    def processDb(self):
        print('procDb')

        if self.current_token.value == '(':
            self.read()
            self.processD()
            if self.current_token.value != ')':
                print("Error: ) is expected")
                return
            self.read()
            print('Db->( D )')
            self.buildTree("()", 1)

        elif self.current_token.type == Tokenizer.TokenType.ID:
            self.read()

            if self.current_token.type == Tokenizer.TokenType.COMMA:
                self.read()
                self.processVb()

                if self.current_token.value != '=':
                    print("Error: = is expected")
                    return
                self.buildTree(",", 2)
                self.read()
                self.processE()
                self.buildTree("=", 2)
            else :
                if self.current_token.value == '=':
                    self.read()
                    self.processE()
                    print('Db->id = E')
                    self.buildTree("=", 2)
                else :
                    n = 0
                    while self.current_token.type == Tokenizer.TokenType.ID or self.current_token.value == '(':
                        self.processVb()
                        n += 1
                    if n == 0:
                        print("Error: ID or ( is expected")
                        return
                    if self.current_token.value != '=':
                        print("Error: = is expected")
                        return
                    self.read()
                    self.processE()
                    print('Db->identifier Vb+ = E')
                    self.buildTree("function_form", n + 2)

    #Defining process Vb
    def processVb(self):
        print('procVb')
        if self.current_token.type == Tokenizer.TokenType.ID:
            self.read()
            print('Vb->id')

        elif self.current_token.value == '(':
            self.read()
            if self.current_token.type == ')':
                print('Vb->( )')
                self.buildTree("()", 0)
                self.read()
            else:
                self.processVL()
                print('Vb->( Vl )')
                if self.current_token.value != ')':
                    print("Error: ) is expected")
                    return
            self.read()

        else:
            print("Error: ID or ( is expected")
            return

    #Defining process Vl
    def processVL(self):
        print("procVL")
        print("559 "+str(self.current_token.value))

        if self.current_token.type != Tokenizer.TokenType.ID:
            print("562 VL: Identifier expected")  
        else:
            print('VL->' + self.current_token.value)

            self.read()
            trees_to_pop = 0
            while self.current_token.value == ',':
                self.read()
                if self.current_token.type != Tokenizer.TokenType.ID:
                    print(" 572 VL: Identifier expected") 
                self.read()
                print('VL->id , ?')

                trees_to_pop += 1
            print('498')
            if trees_to_pop > 0:
                self.buildTree(',', trees_to_pop +1) 

input_path="tests/test_3.txt"
with open(input_path) as file:
    program = file.read()

stack = []
tokens = []
tokenizer = Tokenizer.Tokenizer(program)
token = tokenizer.get_next_token()
print(token.type, token.value)
while token.type != Tokenizer.TokenType.EOF:
    print(token.type, token.value)
    if token.value in Tokenizer.RESERVED_KEYWORDS:
        token.type = Tokenizer.TokenType.RESERVED_KEYWORD

    tokens.append(token)
    token = tokenizer.get_next_token()

screener = Screener(tokens)
tokens = screener.screen()

print(" after screening ")

parser = ASTParser()
parser.tokens = tokens
parser.current_token = tokens[0]
parser.index = 0

parser.processE()
print(len(stack))
root = stack[0]
root.print_tree()
with open(input_path+"_output", "w") as file:
    root.indentation = 0
    root.print_tree_to_file(file)
