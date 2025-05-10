from typing import Any


class VariablesStorage:
    """
    Class to store variables in scope
    """

    __scope_variable: dict[str, dict[str, Any]] = {}

    def __init__(self):
        self.__variables = {}

    def set_variable(self, name: str, value: Any):
        """
        Set a variable in the storage
        :param name: Name of the variable
        :param value: Value of the variable
        """
        self.variables[name] = value

    def get_variable(self, name: str) -> Any:
        """
        Get a variable from the storage
        :param name: Name of the variable
        :return: Value of the variable
        """
        return self.variables.get(name)
