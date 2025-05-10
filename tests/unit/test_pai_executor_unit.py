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

    call increment(10)
    set after_increment to result

    call multiply(3, 4)
    set product to result

    call increment(initial)
    """

    tree = parser.parse(code)
    executor = PaiExecutor(DoNothingPrintStrategy())
    executor.visit(tree)

    assert executor._PaiExecutor__vars["initial"] == 5
    assert executor._PaiExecutor__vars["after_increment"] == 11
    assert executor._PaiExecutor__vars["product"] == 12
    assert executor._PaiExecutor__vars["result"] == 6

    assert "increment" in executor._PaiExecutor__functions
    assert "multiply" in executor._PaiExecutor__functions


def test_nested_function_calls():
    code = """
    tool add(x, y) {
        set result to x + y
    }

    tool calculate(a, b) {
        call add(a, b)
        set intermediate to result
        call add(intermediate, 10)
    }

    call calculate(5, 7)
    """

    tree = parser.parse(code)
    executor = PaiExecutor(DoNothingPrintStrategy())
    executor.visit(tree)

    assert executor._PaiExecutor__vars["result"] == 22
    assert executor._PaiExecutor__vars["intermediate"] == 12


def test_conditional_inside_function():
    code = """
    tool max(a, b) {
        when a > b {
            set result to a
        } otherwise {
            set result to b
        }
    }

    call max(15, 8)
    set max_result1 to result

    call max(3, 9)
    set max_result2 to result
    """

    tree = parser.parse(code)
    executor = PaiExecutor(DoNothingPrintStrategy())
    executor.visit(tree)

    assert executor._PaiExecutor__vars["max_result1"] == 15
    assert executor._PaiExecutor__vars["max_result2"] == 9


def test_function_redefinition():
    code = """
    tool greet() {
        set result to "Hello"
    }

    call greet()
    set first_greeting to result

    tool greet() {
        set result to "Hi"
    }

    call greet()
    """

    tree = parser.parse(code)
    executor = PaiExecutor(DoNothingPrintStrategy())
    executor.visit(tree)

    assert executor._PaiExecutor__vars["first_greeting"] == "Hello"
    assert executor._PaiExecutor__vars["result"] == "Hi"


def test_function_error_handling():
    code_wrong_args = """
    tool sum(a, b) {
        set result to a + b
    }

    call sum(1)
    """

    tree = parser.parse(code_wrong_args)
    executor = PaiExecutor(DoNothingPrintStrategy())

    with pytest.raises(ValueError):
        executor.visit(tree)

    code_undefined = """
    call undefined_function(1, 2)
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

    call modify_local()
    """

    tree = parser.parse(code)
    executor = PaiExecutor(DoNothingPrintStrategy())
    executor.visit(tree)

    assert executor._PaiExecutor__vars["global_var"] == 200
    assert "local_var" not in executor._PaiExecutor__vars
