import Tokenizer
from Tokenizer import Screener
import controlStructure
from CSEMachine import CSEMachine
from ASTNode import ASTNode

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
        if self.current_token.value in  ['true', 'false', 'nil', 'dummy']:
            terminalNode = ASTNode(str(self.current_token.type))
            terminalNode.value = self.current_token.value
            stack.append(terminalNode)
        self.index += 1

        if (self.index < len(self.tokens)):
            self.current_token = self.tokens[self.index]
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
        self.procT()
        if self.current_token.value == 'where':
            self.read()
            self.procDr()
            self.buildTree("where", 2)

    def procT(self):
        self.procTa()
        n = 0
        while self.current_token.value == ',':
            self.read()
            self.procTa()
            n += 1
        if n > 0:
            self.buildTree("tau", n + 1)
        else:
            pass
    def procTa(self):
        self.procTc()
        while self.current_token.value == 'aug':
            self.read()
            self.procTc()
            self.buildTree("aug", 2)

    def procTc(self):
        self.procB()
        if self.current_token.type == Tokenizer.TokenType.TERNARY_OPERATOR:
            self.read()
            self.procTc()

            if self.current_token.value != '|':
                print("Error: | is expected")
                return
            self.read()
            self.procTc()
            self.buildTree("->", 3)

    def procB(self):
        self.procBt()
        while self.current_token.value == 'or':
            self.read()
            self.procBt()
            self.buildTree("or", 2)

    def procBt(self):
        self.procBs()
        while self.current_token.value == '&':
            self.read()
            self.procBs()
            # print('Bt->Bs & Bs')
            self.buildTree("&", 2)

    def procBs(self):
        if self.current_token.value == 'not':
            self.read()
            self.procBp()
            self.buildTree("not", 1)
        else:
            self.procBp()
    def procBp(self):
        self.procA()
        match self.current_token.value:
            case '>':
                self.read()
                self.procA()
                self.buildTree("gr", 2)
            case 'gr':
                self.read()
                self.procA()
                self.buildTree("gr", 2)

            case 'ge':
                self.read()
                self.procA()
                self.buildTree("ge", 2)

            case '>=':
                self.read()
                self.procA()
                self.buildTree("ge", 2)
            case '<':
                self.read()
                self.procA()
                self.buildTree("ls", 2)

            case 'ls':
                self.read()
                self.procA()
                self.buildTree("ls", 2)

            case '<=':
                self.read()
                self.procA()
                self.buildTree("le", 2)

            case 'le':
                self.read()
                self.procA()
                self.buildTree("le", 2)

            case 'eq':
                self.read()
                self.procA()
                self.buildTree("eq", 2)

            case 'ne':
                self.read()
                self.procA()
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


if __name__ == "__main__":
    input_path = 'tests/and'
    with open(input_path) as file:
        program = file.read()

    stack = []
    tokens = []

    tokenizer = Tokenizer.Tokenizer(program)
    token = tokenizer.get_next_token()
    while token.type != Tokenizer.TokenType.EOF:
        tokens.append(token)
        token = tokenizer.get_next_token()

    screener = Screener(tokens)
    tokens = screener.screen()

    parser = ASTParser()
    parser.tokens = tokens
    parser.current_token = tokens[0]
    parser.index = 0

    parser.procE()

    root = stack[0]

    ASTStandarizer = ASTNode("ASTStandarizer")
    root = ASTStandarizer.standarize(root)

    ctrlStructGen = controlStructure.ControlStructureGenerator()
    ctr_structures = ctrlStructGen.generate_control_structures(root)

    cseMachine = CSEMachine(ctr_structures, input_path)
    result = cseMachine.execute()
