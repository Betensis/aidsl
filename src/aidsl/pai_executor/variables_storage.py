from typing import Any, Dict, Optional, List


class VariablesStorage:
    """
    Class to store variables in scope
    """

    def __init__(self):
        # Global scope is the default scope
        self.__scopes = [{}]
        self.__current_scope_index = 0

    def create_scope(self) -> int:
        """
        Create a new scope and return its index
        :return: Index of the new scope
        """
        self.__scopes.append({})
        self.__current_scope_index = len(self.__scopes) - 1
        return self.__current_scope_index

    def switch_to_scope(self, scope_index: int) -> None:
        """
        Switch to a specific scope
        :param scope_index: Index of the scope to switch to
        """
        if 0 <= scope_index < len(self.__scopes):
            self.__current_scope_index = scope_index
        else:
            raise ValueError(f"Scope index {scope_index} is out of range")

    def get_current_scope(self) -> int:
        """
        Get the current scope index
        :return: Current scope index
        """
        return self.__current_scope_index

    def set_variable(self, name: str, value: Any) -> None:
        """
        Set a variable in the current scope
        :param name: Name of the variable
        :param value: Value of the variable
        """
        self.__scopes[self.__current_scope_index][name] = value

    def get_variable(self, name: str) -> Any:
        """
        Get a variable from the current scope or any parent scope
        :param name: Name of the variable
        :return: Value of the variable or None if not found
        """
        # First check in the current scope
        if name in self.__scopes[self.__current_scope_index]:
            return self.__scopes[self.__current_scope_index][name]
        
        # Then check in the global scope if we're not already in it
        if self.__current_scope_index != 0 and name in self.__scopes[0]:
            return self.__scopes[0][name]
        
        return None

    def get_all_variables(self) -> Dict[str, Any]:
        """
        Get all variables accessible from the current scope
        :return: Dictionary of all accessible variables
        """
        # Start with global scope variables
        all_vars = self.__scopes[0].copy()
        
        # Override with current scope variables if not in global scope
        if self.__current_scope_index != 0:
            all_vars.update(self.__scopes[self.__current_scope_index])
            
        return all_vars

    def copy_scope_to_parent(self, variables_to_copy: Optional[List[str]] = None) -> None:
        """
        Copy specified variables from current scope to parent scope
        :param variables_to_copy: List of variable names to copy, if None, copies all
        """
        if self.__current_scope_index <= 0:
            return  # Already in global scope, nothing to do
            
        current_scope = self.__scopes[self.__current_scope_index]
        parent_scope_index = 0  # Always copy to global scope
        
        if variables_to_copy is None:
            # Copy all variables
            for name, value in current_scope.items():
                self.__scopes[parent_scope_index][name] = value
        else:
            # Copy only specified variables
            for name in variables_to_copy:
                if name in current_scope:
                    self.__scopes[parent_scope_index][name] = current_scope[name]

    def remove_scope(self) -> None:
        """
        Remove the current scope and switch to global scope
        """
        if self.__current_scope_index > 0:
            self.__scopes.pop(self.__current_scope_index)
            self.__current_scope_index = 0  # Return to global scope
