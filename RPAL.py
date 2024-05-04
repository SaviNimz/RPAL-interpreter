import Tokenizer
from Tokenizer import Screener
import controlStructure
from CSEMachine import CSEMachine
from ASTNode import ASTNode
from parse import ASTParser



if __name__ == "_main_":

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

    #parser.procE()
    # print(len(stack))
    root = stack[0]

    print(root)
    print("=================================================================================================")
    ASTStandarizer = ASTNode("ASTStandarizer")


    root = ASTStandarizer.standarize(root)

    ctrlStructGen = controlStructure.ControlStructureGenerator()
    ctr_structures = ctrlStructGen.generate_control_structures(root)
        # ctrlStructGen.print_ctrl_structs()

    cseMachine = CSEMachine(ctr_structures, input_path)
    result = cseMachine.execute()

    print(result)
