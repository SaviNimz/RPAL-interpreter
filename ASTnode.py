class ASTNode:


    def standarize(self, root):

        if root == None:
            return None


        root.child = self.standarize(root.child)

        if root.sibling != None:
            root.sibling = self.standarize(root.sibling)

        nextSibling = root.sibling

        # prevSibling = root.previous
        # nextSibling = root.sibling

        match root.type:
            case "let":
                #print("let")
                #print( "type : " , root.child.type)
                if root.child.type == "=":
                    #print("equal")
                    equal = root.child
                    P = equal.sibling
                    X = equal.child
                    E = X.sibling
                    lambdaNode = ASTNode("lambda")
                    gammaNode = ASTNode("gamma")
                    gammaNode.child = lambdaNode
                    lambdaNode.sibling = E
                    #print("stantdarizing let #######")
                    X.sibling = P
                    lambdaNode.child = X
                    # P.previous = X
                    gammaNode.sibling = nextSibling

                    return gammaNode
                else:
                    root.sibling = nextSibling

                    return root
                
            case "where":
                if root.child.sibling.type== "=":
                    P = root.child
                    equal = P.sibling
                    X = equal.child
                    E = X.sibling
                    lambdaNode = ASTNode("lambda")
                    gammaNode = ASTNode("gamma")

                    gammaNode.child = lambdaNode
                    lambdaNode.sibling = E
                    lambdaNode.child = X

                    X.sibling = P
                    # P.previous = gammaNode
                    P.sibling = None

                    gammaNode.sibling = nextSibling


                    return gammaNode
                else:
                    root.sibling = nextSibling

                    return root
                
            case "function_form":
                P = root.child
                V = P.sibling
                Vs = V.sibling

                newRoot = ASTNode("=")
                newRoot.child = P

                lambdaNode = ASTNode("lambda")
                P.sibling = lambdaNode
                lambdaNode.previous = P

                while Vs.sibling != None:
                    lambdaNode.child = V
                    lambdaNode = ASTNode("lambda")
                    V.sibling = lambdaNode
                    lambdaNode.previous = V
                    V = Vs
                    Vs = Vs.sibling

                lambdaNode.child = V
                V.sibling = Vs
                Vs.previous = V

                newRoot.sibling = nextSibling

                return newRoot

