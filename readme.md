# Interpreter for RPAL language

## Introduction

This repository aims to implement a complete interpreter for the RPAL programming language using Python. 
A lexical analyzer and parser for RPAL was developed. The output of our parser will be an Abstract Syntax Tree (AST) representing the input RPAL program. Additionally,  an algorithm has been implemented to convert the AST into a Standardized Tree (ST) and build a Control Stack Environment (CSE) machine. The ultimate goal is to create a program capable of reading an input file containing an RPAL program and generating an output that matches that of "rpal.exe" for the provided program.

![interpreter](https://github.com/SaviNimz/RPAL-interpreter/assets/108650897/0b223583-dfc0-45c1-bdf4-39a4292142ed)


## Module Descriptions
| Module                              | Task                                                                                                   |
| :---------------------------------- | :----------------------------------------------------------------------------------------------------- |
| 1. Tokenizer (Scanner + Screener)  | A lexical analyzer, implemented through a scanner, scans through an input file to generate tokens. It recognizes reserved keywords, eliminates comments and white spaces, and produces an array containing the identified tokens. |
| 2. Abstract Syntax Tree parser      | Iterates through the token sequence and builds an Abstract Syntax Tree. Uses recursive descent parsing to build the tree. |
| 3. Standardizer                     | Standardizes the abstract syntax tree using the given set of standardizing rules.                      |
| 4. Control Structure Generation     | Performs a pre-order traversal of the AST Node while maintaining a FIFO Queue and generates control structures. |
| 5. Control Structure Environment evaluation | Maintains a Control Structure array and a stack. Pops each element in the control structure array and executes a rule based on the stack top and the environment. |


## Installation

1. Clone the repository:
    ```
    https://github.com/SaviNimz/RPAL-interpreter.git
    ```
2. Install Python (if not already installed).
3. Navigate to the project directory:


### File Structure
- **ASTNode.py**: 
    - This section contains the creation, manipulation, and standardization of nodes of the abstract syntax tree.

- **controlStructure.py**: 
    - This section defines the generation and functionality of control structures.

- **CSEMachine.py**: 
    - Implements the Control Stack Environment Machine, which executes the standardized tree.
    - This section iteratively processes control structures and stack operations until completion, managing environment stacks and RPAL-specific functions along the way.

- **Environment.py**: 
    - The Environment class manages environment variables and their values in the RPAL interpreter.

- **RPAL.py**: 
    - Main executable script for the interpreter which contains the parser.

- **Tokenizer.py**: 
    - Handles the tokenization process of the input RPAL program.


## Usage

1. Ensure you have a text file containing the code you want to interpret (e.g: `test_1.txt`).
2. Run the interpreter by executing the following command:
    ```bash
    python myrpal.py file_name
    ```

    Replace `file_name` with the name of the file containing the RPAL program.

3. Optionally, to print only the abstract syntax tree (AST), include the `-ast` switch:
    ```bash
    python myrpal.py file_name -ast
    ```

    This command will parse the RPAL program in `file_name` and print only the AST structure without executing further.


## Example

Suppose you have the following code in `test_1.rpal`:

```python
let x = 10 in
    fn(x) . x + 20
```

Running the interpreter on this code will produce:

```
[Output code]
```