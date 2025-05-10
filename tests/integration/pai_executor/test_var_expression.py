from aidsl.main import get_parser
from aidsl.pai_executor import PaiExecutor
from ...lib.pai_executor import SpyPrintStrategy


def test_variable_with_condition_expressions():
    code = """
    set count to 0
    set condition1 to 0 > 1
    set condition2 to 0 < 1
    set condition3 to 0 = 1

    set condition4 to "test" = "test"
    set condition5 to "test" != "test1"
    set condition6 to "test" != "test"

    print condition1
    print condition2
    print condition3
    print condition4
    print condition5
    print condition6
    """

    print_strategy = SpyPrintStrategy()
    pai_executor = PaiExecutor(print_strategy)
    parser = get_parser()
    tree = parser.parse(code)
    pai_executor.visit(tree)

    assert print_strategy.get_printed_values() == [
        False,
        True,
        False,
        True,
        True,
        False,
    ]
