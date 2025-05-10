from typing import Any, Dict, Optional, List


class VariablesStorage:
    def __init__(self):
        self.__scopes: list[dict[str, Any]] = [{}]
        self.__current_scope_index: int = 0
        self.__global_scope_index: int = 0

    def __is_in_function_scope(self) -> bool:
        return self.__current_scope_index > self.__global_scope_index

    def __variable_exists_in_global_scope(self, name: str) -> bool:
        return name in self.__scopes[self.__global_scope_index]

    def create_scope(self) -> int:
        self.__scopes.append({})
        self.__current_scope_index = len(self.__scopes) - 1
        return self.__current_scope_index

    def switch_to_scope(self, scope_index: int) -> None:
        if 0 <= scope_index < len(self.__scopes):
            self.__current_scope_index = scope_index
        else:
            raise ValueError(f"Scope index {scope_index} is out of range")

    def get_current_scope(self) -> int:
        return self.__current_scope_index

    def set_variable(self, name: str, value: Any) -> None:
        if self.__is_in_function_scope() and self.__variable_exists_in_global_scope(
            name
        ):
            self.__scopes[self.__global_scope_index][name] = value
        else:
            self.__scopes[self.__current_scope_index][name] = value

    def get_variable(self, name: str) -> Any:
        if name in self.__scopes[self.__current_scope_index]:
            return self.__scopes[self.__current_scope_index][name]

        if self.__is_in_function_scope() and self.__variable_exists_in_global_scope(
            name
        ):
            return self.__scopes[self.__global_scope_index][name]

        return None

    def get_all_variables(self) -> Dict[str, Any]:
        all_variables = self.__scopes[self.__global_scope_index].copy()

        if self.__is_in_function_scope():
            all_variables.update(self.__scopes[self.__current_scope_index])

        return all_variables

    def copy_scope_to_parent(
        self, variables_to_copy: Optional[List[str]] = None
    ) -> None:
        if not self.__is_in_function_scope():
            return

        current_scope = self.__scopes[self.__current_scope_index]
        global_scope = self.__scopes[self.__global_scope_index]

        if variables_to_copy is None:
            for name, value in current_scope.items():
                global_scope[name] = value
        else:
            for name in variables_to_copy:
                if name in current_scope:
                    global_scope[name] = current_scope[name]

    def remove_scope(self) -> None:
        if self.__is_in_function_scope():
            self.__scopes.pop(self.__current_scope_index)
            self.__current_scope_index = self.__global_scope_index
