from lark import Transformer, v_args, Token


class ToPythonTypes(Transformer):
    NAME = str
    INT = int

    @v_args(inline=True)
    def string(self, token: Token):
        return token.value[1:-1]

    @v_args(inline=True)
    def int(self, token: Token):
        return int(token)
