import ASTnode


class Tau:
    def __init__(self, n):
        self.n = n
class Beta:
    def __init__(self):
        pass

class CtrlStruct:
    def __init__(self, idx, delta):
        self.idx = idx
        self.delta = delta
class LambdaExpression:
    def __init__(self, envIdx, lambdaIdx, tok):
        self.envIdx = envIdx
        self.lambdaIdx = lambdaIdx
        self.item = tok

    def print_lambda_expression(self):
        if isinstance(self.item, ASTNode.ASTNode):
            pass

        elif isinstance(self.item, list):

            lam_vars = ""
            for it in self.item:

                lam_vars += it.name + ','


class ControlStructureGenerator:
    def __init__(self):
        self.curIdxDelta = 0
        self.queue = []
        self.map_ctrl_structs = {}
        self.current_delta=[]


    def generate_control_structures(self, root):
        delta = []
        self.current_delta = []
        self.pre_order_traversal(root, delta)

        ctrl_delta = CtrlStruct(self.curIdxDelta, delta)
        self.map_ctrl_structs[0] = self.current_delta.copy()


        while len(self.queue)>0:

            self.current_delta = []


            idx, node, delta_queue = self.queue[0]

            self.pre_order_traversal(node, delta_queue)

            ctrl_delta = CtrlStruct(idx, delta_queue)
            self.map_ctrl_structs[idx] = self.current_delta.copy()

            self.queue.pop(0)

        return self.map_ctrl_structs



    def pre_order_traversal(self, root ,delta):

        match root.type :
            case "lambda":

                self.curIdxDelta += 1

                lambda_exp = None
                if root.child.type ==',':

                    tau_list = []
                    child = root.child.child
                    while child is not None:
                        tau_list.append(child)
                        child = child.sibling
                    lambda_exp = LambdaExpression(0, self.curIdxDelta, tau_list)
                else:
                    lambda_exp = LambdaExpression(0, self.curIdxDelta, root.child)
                self.current_delta.append(lambda_exp)
                delta_lambda = []

                self.queue.append((self.curIdxDelta, root.child.sibling, delta_lambda))
                return
            case "->":
                delta2 = []
                savedcurIdxDelta2 = self.curIdxDelta + 1
                savedcurIdxDelta3 = self.curIdxDelta + 2
                self.curIdxDelta += 2

                node2 = root.child.sibling

                node3 = root.child.sibling.sibling

                node2.sibling = None 
                """
                preOrderTraversal(node2, delta2)
                ctrlDelta2 = CtrlStruct(savedcurIdxDelta2, delta2)
                mapCtrlStructs[savedcurIdxDelta2] = ctrlDelta2
                """
                self.queue.append((savedcurIdxDelta2, node2, delta2))

                delta3 = []
                """
                preOrderTraversal(node3, delta3)
                ctrlDelta3 = CtrlStruct(savedcurIdxDelta3, delta3)
                mapCtrlStructs[savedcurIdxDelta3] = ctrlDelta3
                """
                self.queue.append((savedcurIdxDelta3, node3, delta3))
                self.current_delta.append( CtrlStruct ( savedcurIdxDelta2 , delta2))
                self.current_delta.append(CtrlStruct ( savedcurIdxDelta3 , delta3))

                beta = Beta()
                self.current_delta.append(beta) 

                root.child.sibling = None

                self.pre_order_traversal(root.child, delta)

                return
            case "gamma":

                self.current_delta.append(root)
                self.pre_order_traversal(root.child, delta)
                if root.child.sibling is not None:
                    self.pre_order_traversal(root.child.sibling, delta)
                return

            case "tau":
                initial_length=len(self.current_delta)
                node = root.child
                next_node = node.sibling
                deltas_tau = []
                counter = 0
                while node is not None:
                    node.sibling = None
                    self.pre_order_traversal(node, deltas_tau)
                    node = next_node
                    if node is not None:
                        next_node = node.sibling
                    counter += 1

                tau = Tau(counter)
                temp=[]
                final_length=len(self.current_delta)

                counter=final_length-initial_length
                for i in range(counter):
                    temp.append(self.current_delta.pop())

                self.current_delta.append(tau)
                for i in range(counter):
                    self.current_delta.append(temp.pop())

                if root.sibling is not None:
                    self.pre_order_traversal(root.sibling, delta)
                return

            case _ :
                self.current_delta.append(root);
                if (root.child is not None):
                    self.pre_order_traversal(root.child, delta);
                    if (root.child.sibling is not None):
                        self.pre_order_traversal(root.child.sibling, delta);

                return
            