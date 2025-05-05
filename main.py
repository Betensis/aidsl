from functools import cache
from pathlib import Path

import lark


@cache
def get_parser() -> lark.Lark:
    return lark.Lark.open(
        "grammar/main.lark",
        parser="lalr",
        start="start",
        strict=True,
        rel_to= str(Path("./grammar").absolute()),
        debug=True,
    )


if __name__ == "__main__":
    parser = get_parser()
    tree = parser.parse(
        'set count to 0\nset count to "asd"\nwhen 1 equals 1 { set count to "ыфвфыв" } otherwise { set count to 12313 }'
    )
    print(tree.pretty())
