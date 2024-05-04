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

class ASTParser:

    def _int_(self, tokens1):
        self.tokens = tokens1
        self.current_token = None
        self.index = 0

    def read(self):

        if self.current_token.type in [Tokenizer.TokenType.ID, Tokenizer.TokenType.INT,
                                       Tokenizer.TokenType.STRING] :

            terminalNode = ASTNode( str(self.current_token.type))
            terminalNode.value= self.current_token.value
            stack.append(terminalNode)
            # #print stack
            # #print("stack content after reading")
            # for node in stack:
            #     #print(node.data)
        if self.current_token.value in  ['true', 'false', 'nil', 'dummy']:
            # stack.append(ASTNode(self.current_token.value))
            terminalNode = ASTNode(str(self.current_token.type))
            terminalNode.value = self.current_token.value
            stack.append(terminalNode)

        #print("reading : " + str(self.current_token.value))
        self.index += 1

        if (self.index < len(self.tokens)):
            self.current_token = self.tokens[self.index]
        # elif self.index  >=len(self.tokens):



    def buildTree(self, token, ariness):
        global stack
        node = ASTNode(token)

        node.value = None
        node.sourceLineNumber = -1
        node.child = None
        node.sibling = None
        node.previous = None

        while ariness > 0:
            child = stack[-1]
            stack.pop()
            if node.child is not None:
                child.sibling = node.child
                node.child.previous = child
            node.child = child

            node.sourceLineNumber = child.sourceLineNumber
            ariness -= 1

        stack.append(node)
        for node in stack:
            pass
    def procE(self):
        match self.current_token.value:

            case 'let':
                self.read()
                self.procD()

                if self.current_token.value != 'in':
                    return

                self.read()
                self.procE()
                self.buildTree("let", 2)

            case 'fn':

                n = 0

                self.read()

                while self.current_token.type == Tokenizer.TokenType.ID or self.current_token.value == '(':
                    self.procVb()
                    n += 1
                if n == 0:
                    return

                if self.current_token.value != '.':
                    return

                self.read()
                self.procE()
                self.buildTree("lambda", n+1)

            case _:
                self.procEw()

    def procEw(self):
        #print('procEw')
        self.procT()
        # #print('Ew->T')
        if self.current_token.value == 'where':
            self.read()
            self.procDr()
            # #print('Ew->T where Dr')
            self.buildTree("where", 2)

    def procT(self):
        # print('procT')
        self.procTa()
        # print('T->Ta')

        n = 0
        while self.current_token.value == ',':
            self.read()
            self.procTa()
            n += 1
            # print('T->Ta , Ta')
        if n > 0:
            self.buildTree("tau", n + 1)
        else:
            pass
            # print('T->Ta')

    def procTa(self):
        # print('procTa')
        self.procTc()
        # print('Ta->Tc')
        while self.current_token.value == 'aug':
            self.read()
            self.procTc()
            # print('Ta->Tc aug Tc')

            self.buildTree("aug", 2)

    def procTc(self):
        # print('procTc')

        self.procB()
        # print('Tc->B')
        if self.current_token.type == Tokenizer.TokenType.TERNARY_OPERATOR:
            self.read()
            self.procTc()

            if self.current_token.value != '|':
                print("Error: | is expected")
                return
            self.read()
            self.procTc()
            # print('Tc->B -> Tc | Tc')
            self.buildTree("->", 3)

    def procB(self):
        # print('procB')

        self.procBt()
        # print('B->Bt')
        while self.current_token.value == 'or':
            self.read()
            self.procBt()
            # print('B->B or B')
            self.buildTree("or", 2)

    def procBt(self):
        # print('procBt')

        self.procBs()
        # print('Bt->Bs')
        while self.current_token.value == '&':
            self.read()
            self.procBs()
            # print('Bt->Bs & Bs')
            self.buildTree("&", 2)

    def procBs(self):
        # print('procBs')

        if self.current_token.value == 'not':
            self.read()
            self.procBp()
            # print('Bs->not Bp')
            self.buildTree("not", 1)
        else:
            self.procBp()
            # print('Bs->Bp')

    def procBp(self):
        # print('procBp')

        self.procA()
        # print('Bp->A')
        # print(self.current_token.value+"######")

        ##  Bp -> A ( 'gr' | '>') A
        match self.current_token.value:
            case '>':
                self.read()
                self.procA()
                # print('Bp->A gr A')
                self.buildTree("gr", 2)
            case 'gr':
                self.read()
                self.procA()
                # print('Bp->A gr A')
                self.buildTree("gr", 2)

            case 'ge':
                self.read()
                self.procA()
                # print('Bp->A ge A')
                self.buildTree("ge", 2)

            case '>=':
                self.read()
                self.procA()
                # print('Bp->A ge A')
                self.buildTree("ge", 2)



            case '<':
                self.read()
                self.procA()
                # print('Bp->A ls A')
                self.buildTree("ls", 2)

            case 'ls':
                self.read()
                self.procA()
                # print('Bp->A ls A')
                self.buildTree("ls", 2)

            case '<=':
                self.read()
                self.procA()
                # print('Bp->A le A')
                self.buildTree("le", 2)

            case 'le':
                self.read()
                self.procA()
                # print('Bp->A le A')
                self.buildTree("le", 2)

            case 'eq':
                self.read()
                self.procA()
                # print('Bp->A eq A')
                self.buildTree("eq", 2)

            case 'ne':
                self.read()
                self.procA()
                # print('Bp->A ne A')
                self.buildTree("ne", 2)

            case _:
                return

    def procA(self):
        if self.current_token.value == '+':
            self.read()
            self.procAt()
        elif self.current_token.value == '-':
            self.read()
            self.procAt()
            self.buildTree("neg", 1)
        else:
            self.procAt()
        plus = '+'
        while self.current_token.value == '+' or self.current_token.value == '-':

            if self.current_token.value=='-':
                plus='-'

            self.read()
            self.procAt()
            self.buildTree(plus, 2)


    def procAt(self):
        self.procAf()
        while self.current_token.value == '*' or self.current_token.value == '/':
            self.read()
            self.procAf()
            self.buildTree("*", 2)

    def procAf(self):
        self.procAp()
        while self.current_token.value == '**':
            self.read()
            self.procAf()

            self.buildTree("**", 2)

    def procAp(self):
        self.procR()

        while self.current_token.value == '@':
            self.read()
            self.procR()
            self.buildTree("@", 2)

    def procR(self):
        self.procRn()
        while (self.current_token.type in [Tokenizer.TokenType.ID, Tokenizer.TokenType.INT,
                                           Tokenizer.TokenType.STRING] or self.current_token.value in ['true', 'false',
                                                                                                        'nil', 'dummy',
                                                                                                        "("]):
            if self.index >= len(self.tokens):
                break
            self.procRn()
            self.buildTree("gamma", 2)


    def procRn(self):
        if self.current_token.type in [Tokenizer.TokenType.ID, Tokenizer.TokenType.INT,
                                       Tokenizer.TokenType.STRING]:
            self.read()
        elif self.current_token.value in ['true', 'false', 'nil', 'dummy']:
            self.read()
        elif self.current_token.value == '(':
            self.read()
            self.procE()
            if self.current_token.value != ')':
                return
            self.read()

    def procD(self):
        self.procDa()
        while self.current_token.value == 'within':
            self.read()
            self.procD()
            self.buildTree("within", 2)

    def procDa(self):
        self.procDr()
        n = 0
        while self.current_token.value == 'and':
            n += 1
            self.read()
            self.procDa()
        if n > 0:
            self.buildTree("and", n + 1)

    def procDr(self):
        if self.current_token.value == 'rec':
            self.read()
            self.procDb()
            self.buildTree("rec", 1)

        self.procDb()

    def procDb(self):
        if self.current_token.value == '(':
            self.read()
            self.procD()
            if self.current_token.value != ')':
                return
            self.read()
            self.buildTree("()", 1)

        elif self.current_token.type == Tokenizer.TokenType.ID:
            self.read()

            if self.current_token.type == Tokenizer.TokenType.COMMA:
                self.read()
                self.procVb()

                if self.current_token.value != '=':
                    print("Error: = is expected")
                    return
                self.buildTree(",", 2)
                self.read()
                self.procE()
                self.buildTree("=", 2)
            else :
                if self.current_token.value == '=':
                    self.read()
                    self.procE()
                    self.buildTree("=", 2)

                else :
                    n = 0
                    while self.current_token.type == Tokenizer.TokenType.ID or self.current_token.value == '(':
                        self.procVb()
                        n += 1
                    if n == 0:
                        print("Error: ID or ( is expected")
                        return
                    if self.current_token.value != '=':
                        print("Error: = is expected")
                        return
                    self.read()
                    self.procE()
                    self.buildTree("function_form", n + 2)

    def procVb(self):
        if self.current_token.type == Tokenizer.TokenType.ID:
            self.read()
        elif self.current_token.value == '(':
            self.read()

            if self.current_token.type == ')':

                self.buildTree("()", 0)
                self.read()
            else:
                self.procVL()

                if self.current_token.value != ')':
                    print("Error: ) is expected")
                    return
            self.read()
        else:
            print("Error: ID or ( is expected")
            return

    def procVL(self):

        if self.current_token.type != Tokenizer.TokenType.ID:
            pass

        else:
            pass
            self.read()
            trees_to_pop = 0
            while self.current_token.value == ',':
                self.read()
                if self.current_token.type != Tokenizer.TokenType.ID:
                    print("Identifier expected") 
                self.read()

                trees_to_pop += 1
            if trees_to_pop > 0:
                self.buildTree(',', trees_to_pop +1)  
