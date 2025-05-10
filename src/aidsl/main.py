import os
from pathlib import Path

from typer import Typer

from aidsl.pai_executor import PaiExecutor
from aidsl.parser import get_parser

app = Typer()


def _parse_run_path(path: str) -> Path:
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"File {path} does not exist.")
    if not path.is_file():
        raise ValueError(f"Path {path} is not a file.")
    if path.suffix != ".pai":
        raise ValueError(f"File {path} is not a .pai file.")
    if not os.access(path, os.R_OK):
        raise PermissionError(f"File {path} is not readable.")
    if not os.access(path, os.EX_OK):
        raise PermissionError(f"File {path} is not executable.")

    return path


@app.command()
def run(path: str):
    """
    Run the AiDsl script located at the given path.
    """

    parser = get_parser()
    try:
        path = _parse_run_path(path)
    except (FileNotFoundError, ValueError, PermissionError) as e:
        print(f"Error: {e}")
        return
    code = path.read_text()
    try:
        tree = parser.parse(code)
    except Exception as e:
        print(f"Error: {e}")
        return

    executor = PaiExecutor()
    executor.visit(tree)


if __name__ == "__main__":
    app()
