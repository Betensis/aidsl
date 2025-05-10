from aidsl.pai_executor import PaiExecutor
from aidsl.parser import get_parser
from ...lib.pai_executor import SpyPrintStrategy

parser = get_parser()


def test_true_condition_print_expected_value():
    code = """
    when 1 > 0
    {
        print "1 > 0"
    }
    """

    print_strategy = SpyPrintStrategy()
    pai_executor = PaiExecutor(print_strategy)
    tree = parser.parse(code)
    pai_executor.visit(tree)

    assert print_strategy.get_printed_values() == ["1 > 0"]


def test_false_condition_does_not_print():
    code = """
    when 1 < 0
    {
        print "1 < 0"
    }
    """

    print_strategy = SpyPrintStrategy()
    pai_executor = PaiExecutor(print_strategy)
    tree = parser.parse(code)
    pai_executor.visit(tree)

    assert print_strategy.get_printed_values() == []
