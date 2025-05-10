from aidsl.pai_executor import PaiExecutor, DoNothingPrintStrategy
from aidsl.parser import get_parser

parser = get_parser()


def test_pai_executor_can_parse_var_condition_print():
    code = """
    set count to 0
    when count = 0
    {
        print "count is zero"
    }
    otherwise
    {
        set count to 1
        print "count is one"
    }

    print count
    """
    
    tree = parser.parse(code)
    executor = PaiExecutor(DoNothingPrintStrategy())
    executor.visit(tree)
    assert True
