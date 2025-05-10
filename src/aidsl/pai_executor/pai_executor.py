from lark import Tree
from lark.visitors import Interpreter, Discard

from aidsl.expression.evaluator import ExpressionEvaluator
from aidsl.pai_executor.print_strategy import PrintStrategy, ConsolePrintStrategy


class PaiExecutor(Interpreter):
    def __init__(self, print_strategy: PrintStrategy = ConsolePrintStrategy()):
        self.__vars = {}
        self.__print_strategy = print_strategy
        self.__functions = {}
        self.__return_value = None
        self.__is_returning = False

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
            if self.__is_returning:
                break

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



    def function_call(self, tree: Tree):
        func_name = str(tree.children[0])
        args = []
        for arg in tree.children[1:]:
            if arg is not None:
                args.append(ExpressionEvaluator(self.__vars).visit(arg))

        return self._execute_function(func_name, args)

    def function_call_expr(self, tree: Tree):
        return self.function_call(tree.children[0])

    def return_stmt(self, tree: Tree):
        expr = tree.children[0]
        value = ExpressionEvaluator(self.__vars).visit(expr)
        self.__return_value = value
        self.__is_returning = True
        return Discard

    def _execute_function(self, func_name, args):
        if func_name not in self.__functions:
            raise ValueError(f"Function '{func_name}' is not defined")

        func_info = self.__functions[func_name]
        params = func_info["params"]

        if len(args) != len(params):
            raise ValueError(
                f"Function '{func_name}' expects {len(params)} arguments, got {len(args)}"
            )

        old_vars = self.__vars.copy()
        old_is_returning = self.__is_returning
        old_return_value = self.__return_value
        
        # Reset return state for this function call
        self.__is_returning = False
        self.__return_value = None
        
        for param_name, arg_value in zip(params, args):
            self.__vars[param_name] = arg_value

        self.visit(func_info["block"])

        # Check if we have a return value from the function
        return_value = self.__return_value
        
        # If no explicit return, fall back to the 'result' variable
        if return_value is None:
            return_value = self.__vars.get("result")
        
        intermediate_value = self.__vars.get("intermediate")

        for key in list(self.__vars.keys()):
            if key not in old_vars or key in ("result", "intermediate"):
                continue
            old_vars[key] = self.__vars[key]

        self.__vars = old_vars
        
        # Restore previous return state
        self.__is_returning = old_is_returning
        self.__return_value = old_return_value

        if return_value is not None:
            self.__vars["result"] = return_value
        if intermediate_value is not None:
            self.__vars["intermediate"] = intermediate_value

        return return_value
