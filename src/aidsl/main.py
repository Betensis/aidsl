from aidsl.pai_executor import PaiExecutor


if __name__ == "__main__":
    parser = get_parser()
    with open("test.pai", "r") as f:
        code = f.read()
    tree = parser.parse(code)
    PaiExecutor().visit(tree)
