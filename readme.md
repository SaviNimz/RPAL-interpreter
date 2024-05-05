# Interpreter for RPAL language

## Introduction

This repository contains an interpreter for RPAL programming language implemented in Python. Currently this repository only contains working modules for tokenizer and parser which outputs an abstract syntax tree (AST).

## Features

- **Tokenizer:** Tokenizes input code into tokens such as identifiers, integers, strings, and reserved keywords.
- **Parser:** Parses the tokenized input code and generates an abstract syntax tree (AST) representing the structure of the code.
- **Abstract Syntax Tree (AST):** Represents the hierarchical structure of the code, facilitating further analysis and interpretation.

## Installation

1. Clone the repository:
    ```
    https://github.com/SaviNimz/RPAL-interpreter.git
    ```
2. Install Python (if not already installed).
3. Navigate to the project directory:

## Code Insights
![interpreter](https://github.com/SaviNimz/RPAL-interpreter/assets/108650897/0b223583-dfc0-45c1-bdf4-39a4292142ed)

## Usage

1. Ensure you have a text file containing the code you want to interpret (e.g., `test_1.txt`).
2. Run the interpreter by executing the following command:
    ```
    python parser.py
    ```
3. The interpreter will tokenize the input code, parse it, generate the abstract syntax tree (AST), and print the AST structure.

## Example

Suppose you have the following code in `test_1.txt`:

```python
let x = 10 in
    fn(x) . x + 20

Running the interpreter on this code will produce the following AST:

let
. id:x
. 10
fn
. id:x
+ 
. id:x
. 20


