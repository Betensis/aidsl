from pathlib import Path

import pytest

from aidsl.pai_executor import PaiExecutor
from aidsl.pai_executor.print_strategy import DoNothingPrintStrategy
from aidsl.parser import get_parser

parser = get_parser()


def test_pai_executor_can_parse_condition():
    code = """
    when 1 = 1
    {
    }

    when 1 = 1
    {
    }
    otherwise
    {
    }

    when 5 < 3
    {
    }

    when 5 < 3
    {
    }
    otherwise
    {
    }

    when 5 > 3
    {
    }
    otherwise
    {
    }
    """

    tree = parser.parse(code)
    executor = PaiExecutor(DoNothingPrintStrategy())
    executor.visit(tree)
    assert True


def test_pai_executor_can_parse_print():
    code = """
    print "Test!"
    print "LALA"
    print 1
    """

    tree = parser.parse(code)
    executor = PaiExecutor(DoNothingPrintStrategy())
    executor.visit(tree)
    assert True


def test_pai_executor_can_parse_set_variable():
    code = """
    set count to 0
    set count13 to "Test"

    set alert to "asd"
    set alert to 123

    set boolean to true
    set boolean to false

    set expression to 1 > 0
    set expression to count < 1
    set expression to count = 0
    """

    tree = parser.parse(code)
    executor = PaiExecutor(DoNothingPrintStrategy())
    executor.visit(tree)
    assert True


def test_pai_executor_can_handle_functions():
    code = """
    set initial to 5

    tool increment(value) {
        set result to value + 1
    }

    tool multiply(a, b) {
        set result to a * b
    }

    increment(10)
    set after_increment to result

    multiply(3, 4)
    set product to result

    increment(initial)
    """

    tree = parser.parse(code)
    executor = PaiExecutor(DoNothingPrintStrategy())
    executor.visit(tree)

    vars_dict = executor._PaiExecutor__vars_storage.get_all_variables()
    assert vars_dict["initial"] == 5
    assert vars_dict["after_increment"] == 11
    assert vars_dict["product"] == 12
    assert vars_dict["result"] == 6

    assert "increment" in executor._PaiExecutor__functions
    assert "multiply" in executor._PaiExecutor__functions


def test_nested_function_calls():
    code = """
    tool add(x, y) {
        set result to x + y
    }

    tool calculate(a, b) {
        add(a, b)
        set intermediate to result
        add(intermediate, 10)
    }

    calculate(5, 7)
    """

    tree = parser.parse(code)
    executor = PaiExecutor(DoNothingPrintStrategy())
    executor.visit(tree)

    vars_dict = executor._PaiExecutor__vars_storage.get_all_variables()
    assert vars_dict["result"] == 22
    assert vars_dict["intermediate"] == 12


def test_conditional_inside_function():
    code = """
    tool max(a, b) {
        when a > b {
            set result to a
        } otherwise {
            set result to b
        }
    }

    max(15, 8)
    set max_result1 to result

    max(3, 9)
    set max_result2 to result
    """

    tree = parser.parse(code)
    executor = PaiExecutor(DoNothingPrintStrategy())
    executor.visit(tree)

    vars_dict = executor._PaiExecutor__vars_storage.get_all_variables()
    assert vars_dict["max_result1"] == 15
    assert vars_dict["max_result2"] == 9


def test_function_redefinition():
    code = """
    tool greet() {
        set result to "Hello"
    }

    greet()
    set first_greeting to result

    tool greet() {
        set result to "Hi"
    }

    greet()
    """

    tree = parser.parse(code)
    executor = PaiExecutor(DoNothingPrintStrategy())
    executor.visit(tree)

    vars_dict = executor._PaiExecutor__vars_storage.get_all_variables()
    assert vars_dict["first_greeting"] == "Hello"
    assert vars_dict["result"] == "Hi"


def test_return_statement():
    code = """
    tool add(a, b) {
        return a + b
    }

    add(5, 7)
    set sum_result to result
    
    tool get_message() {
        return "Hello World"
    }
    
    get_message()
    set message to result
    
    tool early_return(x) {
        when x > 10 {
            return "Greater than 10"
        }
        return "Less than or equal to 10"
    }
    
    early_return(15)
    set result1 to result
    
    early_return(5)
    set result2 to result
    """

    tree = parser.parse(code)
    executor = PaiExecutor(DoNothingPrintStrategy())
    executor.visit(tree)

    vars_dict = executor._PaiExecutor__vars_storage.get_all_variables()
    assert vars_dict["sum_result"] == 12
    assert vars_dict["message"] == "Hello World"
    assert vars_dict["result1"] == "Greater than 10"
    assert vars_dict["result2"] == "Less than or equal to 10"


def test_function_error_handling():
    code_wrong_args = """
    tool sum(a, b) {
        set result to a + b
    }

    sum(1)
    """

    tree = parser.parse(code_wrong_args)
    executor = PaiExecutor(DoNothingPrintStrategy())

    with pytest.raises(ValueError):
        executor.visit(tree)

    code_undefined = """
    undefined_function(1, 2)
    """

    tree = parser.parse(code_undefined)
    executor = PaiExecutor(DoNothingPrintStrategy())

    with pytest.raises(ValueError):
        executor.visit(tree)


def test_local_variable_isolation():
    code = """
    set global_var to 100

    tool modify_local() {
        set local_var to 42
        set global_var to 200
    }

    modify_local()
    """

    tree = parser.parse(code)
    executor = PaiExecutor(DoNothingPrintStrategy())
    executor.visit(tree)

    vars_dict = executor._PaiExecutor__vars_storage.get_all_variables()
    assert vars_dict["global_var"] == 200
    assert "local_var" not in vars_dict


def test_variable_scoping():
    code = """
    set global_var to "global"
    
    tool outer_function() {
        set outer_var to "outer"
        
        tool inner_function() {
            set inner_var to "inner"
            set global_var to "modified in inner"
            return inner_var + " " + outer_var + " " + global_var
        }
        
        inner_function()
        print "Result from nested function: "
        print result
        return result + " from outer"
    }
    
    outer_function()
    set final_result to result
    """
    
    tree = parser.parse(code)
    executor = PaiExecutor(DoNothingPrintStrategy())
    executor.visit(tree)
    
    vars_dict = executor._PaiExecutor__vars_storage.get_all_variables()
    assert vars_dict["global_var"] == "modified in inner"
    assert vars_dict["final_result"] == "inner outer modified in inner from outer"
    assert "outer_var" not in vars_dict
    assert "inner_var" not in vars_dict

def test_execute_complex_test_pai():
    test_file_path = Path(__file__).parent / "test_data" / "test.pai"
    assert test_file_path.exists(), f"File {test_file_path} does not exist"
    code = test_file_path.read_text()
    parser = get_parser()
    tree = parser.parse(code)
    executor = PaiExecutor()
    executor.visit(tree)
    assert True
