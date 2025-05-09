from pathlib import Path

from main import get_parser
from pai_executor import PaiExecutor, DoNothingPrintStrategy

parser = get_parser()

tested_data_dir = Path(__file__).parent.joinpath("tested_data")


def test_pai_executor_can_parse_correct_code():
    for pai_file in tested_data_dir.iterdir():
        if pai_file.suffix == ".pai":
            with open(pai_file, "r") as f:
                code = f.read()
            tree = parser.parse(code)
            executor = PaiExecutor(DoNothingPrintStrategy())
            executor.visit(tree)
            assert True
