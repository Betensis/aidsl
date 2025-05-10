from lark import Tree
from lark.visitors import Interpreter

from aidsl.expression.evaluator import ExpressionEvaluator
from aidsl.pai_executor.print_strategy import PrintStrategy, ConsolePrintStrategy


class PaiExecutor(Interpreter):
    def __init__(self, print_strategy: PrintStrategy = ConsolePrintStrategy()):
        self.__vars = {}
        self.__print_strategy = print_strategy
        self.__functions = {}

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

    def tool_stmt(self, tree: Tree):
        name = str(tree.children[0])
        params = self.visit(tree.children[1])
        block = tree.children[2]

        self.__functions[name] = {"params": params, "block": block}

    def params(self, tree: Tree):
        if not tree.children or not all(tree.children):
            return []
        return [str(param.children[0]) for param in tree.children if param]

    def param(self, tree: Tree):
        return tree

    def call_stmt(self, tree: Tree):
        func_name = str(tree.children[0])
        args = []
        for arg in tree.children[1:]:
            if arg is not None:
                args.append(ExpressionEvaluator(self.__vars).visit(arg))

        if func_name not in self.__functions:
            raise ValueError(f"Function '{func_name}' is not defined")

        func_info = self.__functions[func_name]
        params = func_info["params"]

        if len(args) != len(params):
            raise ValueError(
                f"Function '{func_name}' expects {len(params)} arguments, got {len(args)}"
            )

        old_vars = self.__vars.copy()
        for param_name, arg_value in zip(params, args):
            self.__vars[param_name] = arg_value

        self.visit(func_info["block"])

        result_value = self.__vars.get("result")
        intermediate_value = self.__vars.get("intermediate")

        for key in list(self.__vars.keys()):
            if key not in old_vars or key in ("result", "intermediate"):
                continue
            old_vars[key] = self.__vars[key]

        self.__vars = old_vars

        if result_value is not None:
            self.__vars["result"] = result_value
        if intermediate_value is not None:
            self.__vars["intermediate"] = intermediate_value
