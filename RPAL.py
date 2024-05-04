import Tokenizer
from Tokenizer import Screener
import controlStructure
from CSEMachine import CSEMachine
from ASTNode import ASTNode
from parse import ASTParser

import sys

if len(sys.argv) > 1:
    argv_idx = 1  
    ast_flag = 0  

    if len(sys.argv) == 3:  
        argv_idx = 2
        if sys.argv[2] == "-ast":  
            print("AST flag is set")
            ast_flag = 1

        input_path = sys.argv[1]
    else:
        input_path = sys.argv[1]

numeric_result_file=["test_cases/standarizer","test_cases/sum"]
test_results=[]
test_id=0

with open("tests/test_2.txt") as file:
    program = file.read()

stack = []
tokens = []

tokenizer = Tokenizer.Tokenizer(program)
token = tokenizer.getNextToken()
while token.type != Tokenizer.TokenType.EOF:
    tokens.append(token)
    token = tokenizer.getNextToken()

screener = Screener(tokens)
tokens = screener.screen()

parser = ASTParser()
parser.tokens = tokens
parser.current_token = tokens[0]
parser.index = 0

parser.processE()

root = stack[0]

with open( "tests/test_2.txt", "w") as file:
    root.indentation = 0
    root.print_tree_to_file(file)
    if ast_flag == 1: root.print_tree_to_cmd()

print('hello world')
if ast_flag == 0:
    ASTStandarizer = ASTNode("ASTStandarizer")
    root= ASTStandarizer.standarize(root)

    with open(input_path+"__standarized_output", "w") as file:
        root.indentation = 0
        root.print_tree_to_file(file)

    ctrlStructGen = controlStructure.ControlStructureGenerator()
    ctr_structures=ctrlStructGen.generate_control_structures(root)
    cseMachine= CSEMachine(ctr_structures ,input_path)
    result=cseMachine.execute()

    for t in test_results:
        id+=1