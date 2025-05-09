from functools import cache
from pathlib import Path

import lark

from lark import Transformer, v_args, Token

from lark import Tree
from lark.visitors import Interpreter


class PaiExecutor(Interpreter):
    def __init__(self):
        self.__vars = {}

    def assign_stmt(self, tree: Tree):
        name, value = tree.children
        self.__vars[str(name)] = ToPythonTypes().transform(value)

    def when_stmt(self, tree: Tree):
        comp = tree.children[0]
        true_blk = tree.children[1]
        false_blk = tree.children[2] if len(tree.children) == 3 else None

        if self.visit(comp):
            self.visit(true_blk)
        elif false_blk:
            self.visit(false_blk)

    def log_stmt(self, tree: Tree):
        tree = ToPythonTypes().transform(tree)
        value = tree.children[0]
        if isinstance(value, (int, str)):
            print(value)
            return

        token: Token = value.children[0]
        if (isinstance(value, Tree) and value.data == "name"):
            print(self.__vars.get(str(token)))

    def comparison(self, tree: Tree):
        left, right = tree.children
        if isinstance(left, Tree) and left.data == "name":
            left = self.__vars.get(str(left.children[0]))
        else:
            right = ToPythonTypes().transform(right)
        if isinstance(right, Tree) and right.data == "name":
            right = self.__vars.get(str(right.children[0]))
        else:
            right = ToPythonTypes().transform(right)

        return left == right

    def block(self, tree: Tree):
        for stmt in tree.children:
            self.visit(stmt)

    def start(self, tree: Tree):
        for stmt in tree.children:
            self.visit(stmt)


class ToPythonTypes(Transformer):
    NAME = str
    INT = int

    @v_args(inline=True)
    def string(self, token: Token):
        return token.value[1:-1]

    @v_args(inline=True)
    def int(self, token: Token):
        return int(token)

@cache
def get_parser() -> lark.Lark:
    return lark.Lark.open(
        "grammar/main.lark",
        parser="lalr",
        start="start",
        rel_to=str(Path("./grammar").absolute()),
        debug=True,
    )


if __name__ == "__main__":
    parser = get_parser()
    with open('test.pai', 'r') as f:
        code = f.read()
    tree = parser.parse(code)
    PaiExecutor().visit(tree)
