import ast

"""
documentation: https://docs.python.org/3/library/ast.html#
"""
class NodeVisiter(ast.NodeVisitor):
    """
    A custom AST visitor that visit different kind of node
    """
    def __init__(self):
        super().__init__()
        self.list_items = []
        
    def visit_Assign(self, node):
        # check what in the list
        if isinstance(node.value, ast.List):
            #print(node.targets[0].id) # get list name
            for elem in node.value.elts: # get list value
                #print(elem.value)
                self.list_items.append(elem.value)
        self.generic_visit(node)
        return node
    
    def visit_If(self, node):
        """
        Visits each 'if' node in the AST and instruments it for branch coverage.
        """
        """
        print(node.body)
        if isinstance(node.body[0], ast.Return):
            print(node.body[0].value.value)
        try:
            print("node name: " + str(node.test.comparators[0]))
            condition = node.test.comparators  # Accessing the condition inside the If node
            for con in condition:
                print(con)
                try:
                    print(con.value)
                except Exception:
                    continue
        except:
            pass
        """
        self.generic_visit(node)  # Visit all other node types
        return node

if __name__ == "__main__":
    v = ast.parse(open("test.py", 'r').read())
    visitor = NodeVisiter()
    visitor.visit(v)
    print(visitor.list_items)