from lark import Tree
from lark.visitors import Interpreter


class ExpressionEvaluator(Interpreter):
    def __init__(self, variables: dict):
        self.__vars = variables

    def comparison_expr(self, tree: Tree):
        left_expr, op_node, right_expr = tree.children
        left = self.visit(left_expr)
        right = self.visit(right_expr)

        operation = op_node.data

        if operation == "equal":
            return left == right
        elif operation == "more":
            return left > right
        elif operation == "less":
            return left < right
        else:
            raise ValueError(f"Unknown operation: {operation}")

    @staticmethod
    def int(tree: Tree):
        return int(tree.children[0])

    @staticmethod
    def string(tree: Tree):
        token = tree.children[0]
        return token[1:-1]

    def name(self, tree: Tree):
        varname = str(tree.children[0])
        return self.__vars.get(varname)

    @staticmethod
    def true(_):
        return True

    @staticmethod
    def false(_):
        return False
