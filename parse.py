from scanner import tokenize_file

file_path = 'input.rpal'
tokens = tokenize_file(file_path)

# source line number is useful for error handling, debugging, and generating meaningful error messages.
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

# we can use the following class to create stacks 
        
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