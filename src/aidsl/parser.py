from functools import cache
from pathlib import Path

import lark


@cache
def get_parser() -> lark.Lark:
    project_root = Path(__file__).parent.parent.parent
    grammar_dir = project_root / "grammar"
    main_grammar = grammar_dir / "main.lark"

    return lark.Lark.open(
        str(main_grammar),
        parser="lalr",
        start="start",
        rel_to=str(grammar_dir),
        debug=True,
    )
