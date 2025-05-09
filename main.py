from functools import cache
from pathlib import Path

import lark

from pai_executor import PaiExecutor


@cache
def get_parser() -> lark.Lark:
    project_root = Path(__file__).parent
    grammar_dir = project_root / "grammar"
    main_grammar = grammar_dir / "main.lark"

    return lark.Lark.open(
        str(main_grammar),
        parser="lalr",
        start="start",
        rel_to=str(grammar_dir),
        debug=True,
    )


if __name__ == "__main__":
    parser = get_parser()
    with open("test.pai", "r") as f:
        code = f.read()
    tree = parser.parse(code)
    PaiExecutor().visit(tree)
