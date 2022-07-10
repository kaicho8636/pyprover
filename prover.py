then_symbol = '->'
and_symbol = '/\\'
or_symbol = '\\/'


class Prover:
    def __init__(self, goal):
        self.goal = goal
        self.variables = []
        self.subgoals = []  # [(goal, variables), ...]

    def assumption(self):
        if self.goal in self.variables:
            self.goal = None
            if self.subgoals:
                (self.goal, self.variables) = self.subgoals.pop()
            return False
        else:
            return True

    def intro(self):
        if self.goal.symbol == then_symbol:
            self.variables.append(self.goal.left)
            self.goal = self.goal.right
            return False
        else:
            return True

    def apply(self, number):
        if len(self.variables) <= number:
            return True
        elif (self.variables[number].symbol == then_symbol
                and self.variables[number].right == self.goal):
            self.goal = self.variables[number].left
            return False
        else:
            return True

    def split(self):
        if self.goal.symbol == and_symbol:
            self.subgoals.append((self.goal.right, self.variables))
            self.goal = self.goal.left
            return False
        else:
            return True

    def left(self):
        if self.goal.symbol == or_symbol:
            self.goal = self.goal.left
            return False
        else:
            return True

    def right(self):
        if self.goal.symbol == or_symbol:
            self.goal = self.goal.right
            return False
        else:
            return True

    def destruct(self, number):
        if len(self.variables) <= number:
            return True
        elif self.variables[number].symbol == and_symbol:
            self.variables.append(self.variables[number].left)
            self.variables.append(self.variables[number].right)
            del self.variables[number]
            return False
        elif self.variables[number].symbol == or_symbol:
            temp = self.variables
            temp[number] = temp[number].right
            self.subgoals.append((self.goal, temp))
            self.variables[number] = self.variables[number].left
            return False
        else:
            return True

    def qed(self):
        return
