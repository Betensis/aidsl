from lark import Tree
from lark.visitors import Interpreter


class ExpressionEvaluator(Interpreter):
    def __init__(self, variables: dict):
        self.__vars = variables

    def int(self, tree: Tree):
        return int(tree.children[0])

    def string(self, tree: Tree):
        token = tree.children[0]
        return token[1:-1]

    def name(self, tree: Tree):
        varname = str(tree.children[0])
        return self.__vars.get(varname)
