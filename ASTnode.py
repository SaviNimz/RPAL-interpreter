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