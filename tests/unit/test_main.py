import lark
import pytest

from aidsl.main import get_parser


def test_returns_lark_instance_for_valid_grammar():
    parser = get_parser()
    assert isinstance(parser, lark.Lark)


def test_raises_file_not_found_for_missing_grammar(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(
        "lark.Lark.open", lambda *a, **kw: (_ for _ in ()).throw(FileNotFoundError())
    )
    with pytest.raises(FileNotFoundError):
        get_parser.cache_clear()
        get_parser()
