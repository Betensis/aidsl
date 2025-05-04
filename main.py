import lark


if __name__ == "__main__":
    parser = lark.Lark.open("main.lark", parser="lalr", start="start", rel_to=__file__)
    tree = parser.parse("set count to 0\nset count to \"asd\"\nwhen 1 equals 1 {} otherwise {}")
    print(tree)
