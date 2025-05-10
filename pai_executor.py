from abc import ABC, abstractmethod

from lark import Tree
from lark.visitors import Interpreter

from expression.evaluator import ExpressionEvaluator
from procols import Printable


class PrintStrategy(ABC):
    @abstractmethod
    def print(self, value: Printable):
        pass


class ConsolePrintStrategy(PrintStrategy):
    def print(self, value: Printable):
        print(value)


class DoNothingPrintStrategy(PrintStrategy):
    def print(self, value: Printable):
        pass


class PaiExecutor(Interpreter):
    def __init__(self, print_strategy: PrintStrategy = ConsolePrintStrategy()):
        self.__vars = {}
        self.__print_strategy = print_strategy

    def assign_stmt(self, tree: Tree):
        name, expr = tree.children
        value = ExpressionEvaluator(self.__vars).visit(expr)
        self.__vars[str(name)] = value

    def when_stmt(self, tree: Tree):
        cond_expr = tree.children[0]
        true_blk = tree.children[1]
        false_blk = tree.children[2] if len(tree.children) == 3 else None

        condition_result = ExpressionEvaluator(self.__vars).visit(cond_expr)

        if condition_result:
            self.visit(true_blk)
        elif false_blk:
            self.visit(false_blk)

    def comparison(self, tree: Tree):
        left_expr, op_node, right_expr = tree.children
        left = ExpressionEvaluator(self.__vars).visit(left_expr)
        right = ExpressionEvaluator(self.__vars).visit(right_expr)

        operation = op_node.data

        if operation == "equal":
            return left == right
        elif operation == "more":
            return left > right
        elif operation == "less":
            return left < right
        else:
            raise ValueError(f"Unknown operation: {operation}")

    def print_stmt(self, tree: Tree):
        expr = tree.children[0]
        value = ExpressionEvaluator(self.__vars).visit(expr)
        self.__print_strategy.print(value)

    def block(self, tree: Tree):
        for stmt in tree.children:
            self.visit(stmt)

    def start(self, tree: Tree):
        for stmt in tree.children:
            self.visit(stmt)
