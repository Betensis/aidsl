from functools import cache
from pathlib import Path

import lark

from pai_executor import PaiExecutor


@cache
def get_parser() -> lark.Lark:
    return lark.Lark.open(
        "grammar/main.lark",
        parser="lalr",
        start="start",
        rel_to=str(Path("./grammar").absolute()),
        debug=True,
    )


if __name__ == "__main__":
    parser = get_parser()
    with open("test.pai", "r") as f:
        code = f.read()
    tree = parser.parse(code)
    PaiExecutor().visit(tree)
