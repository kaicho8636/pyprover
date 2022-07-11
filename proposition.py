from lark import Lark, Transformer, v_args


then_symbol = '→'
and_symbol = '∧'
or_symbol = '∨'


class PropNameError(Exception):
    pass


@v_args(inline=True)
class PropParseTree(Transformer):
    def __init__(self, prop_vars):
        super().__init__()
        self.prop_vars = prop_vars

    def l_then(self, a, b):
        return PropNode("→", a, b)

    def l_and(self, a, b):
        return PropNode("∧", a, b)

    def l_or(self, a, b):
        return PropNode("∨", a, b)

    def l_not(self, a):
        return PropNode("→", a, PropNode("False"))

    def identifier(self, symbol):
        if symbol in self.prop_vars:
            return PropNode(symbol)
        else:
            raise PropNameError(f"Propositional variable '{symbol}' not defined")

    def l_true(self):
        return PropNode("True")

    def l_false(self):
        return PropNode("False")


with open("proposition.lark", "r", encoding="utf-8") as grammar:
    parser = Lark(grammar, parser="lalr")


class PropNode:
    def __init__(self, symbol, left=None, right=None):
        self.symbol = symbol
        self.left = left
        self.right = right

    def __str__(self):
        if self.left is None or self.right is None:
            return self.symbol
        else:
            return '(' + str(self.left) + ' ' + self.symbol + ' ' + str(self.right) + ')'

    def __eq__(self, other):
        return self.symbol == other.symbol and self.left == other.left and self.right == other.right

    def get_vars(self):
        if self.symbol in [and_symbol, or_symbol, then_symbol]:
            return self.left.get_vars() + self.right.get_vars()
        elif self.symbol in ['False', 'True']:
            return []
        else:
            return [self.symbol]

    def evaluate(self, dictionary):
        if self.symbol == and_symbol:
            return self.left.evaluate(dictionary) and self.right.evaluate(dictionary)
        elif self.symbol == or_symbol:
            return self.left.evaluate(dictionary) or self.right.evaluate(dictionary)
        elif self.symbol == then_symbol:
            return not self.left.evaluate(dictionary) or self.left.evaluate(dictionary)
        elif self.symbol == 'False':
            return False
        elif self.symbol == 'True':
            return True
        else:
            return dictionary[self.symbol]

    def is_tautology(self):
        patterns = [[]]
        variables = self.get_vars()
        for _ in variables:
            patterns = [pattern+[i] for i in [False, True] for pattern in patterns]
        for pattern in patterns:
            if not self.evaluate({var: b for var, b in zip(variables, pattern)}):
                return False
        return True
