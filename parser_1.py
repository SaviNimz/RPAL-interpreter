def is_current_token():
    pass

def procE():
    print("procE")
    if (is_current_token=("KEYWORD","let")):
        #read the non-terminal function
        readNT()
        procD()
        if (is_current_token!=("KEYWORD","in")):
            print("E: 'in' expected")
            exit(0)
        #read the non-terminal function
        readNT()
        procE()
        buildNAryASTNode()#IDK WHAT TO PASS

    else if (is_current_token=("KEYWORD","fn")):
        #tree pop function call?
        readNT()
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
    if(is_current_token=("KEYWORD","where")):
        readNT()
        procDR()
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