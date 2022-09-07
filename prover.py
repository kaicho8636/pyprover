from copy import deepcopy
from proposition import PropNode, then_symbol, and_symbol, or_symbol


def dn(prop):
    return PropNode("→", PropNode("→", prop, PropNode("False")), PropNode("False"))


class Prover:
    def __init__(self, goal: PropNode):
        self.goal = goal
        self.variables = []
        self.subgoals = []  # [(goal, variables), ...]
        self.undos = []

    def __set_undo(self):
        self.undos.append(deepcopy((self.goal, self.variables, self.subgoals)))

    def undo(self) -> bool:
        if not self.undos:
            return True
        else:
            (self.goal, self.variables, self.subgoals) = self.undos.pop()
            return False

    def assumption(self) -> bool:
        self.__set_undo()
        if self.goal in self.variables:
            self.goal = None
            if self.subgoals:
                (self.goal, self.variables) = self.subgoals.pop()
            return False
        else:
            return True

    def intro(self) -> bool:
        self.__set_undo()
        if self.goal.symbol == then_symbol:
            self.variables.append(self.goal.left)
            self.goal = self.goal.right
            return False
        else:
            return True

    def apply(self, number) -> bool:
        self.__set_undo()
        if len(self.variables) <= number:
            return True
        elif (self.variables[number].symbol == then_symbol
              and self.variables[number].right == self.goal):
            self.goal = self.variables[number].left
            return False
        else:
            return True

    def split(self) -> bool:
        self.__set_undo()
        if self.goal.symbol == and_symbol:
            self.subgoals.append((self.goal.right, self.variables))
            self.goal = self.goal.left
            return False
        else:
            return True

    def left(self):
        self.__set_undo()
        if self.goal.symbol == or_symbol:
            self.goal = self.goal.left
            return False
        else:
            return True

    def right(self):
        self.__set_undo()
        if self.goal.symbol == or_symbol:
            self.goal = self.goal.right
            return False
        else:
            return True

    def destruct(self, number) -> bool:
        self.__set_undo()
        if len(self.variables) <= number:
            return True
        elif self.variables[number].symbol == and_symbol:
            self.variables.append(self.variables[number].left)
            self.variables.append(self.variables[number].right)
            del self.variables[number]
            return False
        elif self.variables[number].symbol == or_symbol:
            temp = self.variables[:]
            temp[number] = temp[number].right
            self.subgoals.append((self.goal, temp))
            self.variables[number] = self.variables[number].left
            return False
        else:
            return True

    def specialize(self, function, domain) -> bool:
        self.__set_undo()
        if len(self.variables) <= min(function, domain):
            return True
        elif (self.variables[function].symbol != "→"
              or self.variables[function].left != self.variables[domain]):
            return True
        else:
            self.variables[function] = self.variables[function].right
            return False

    def add_dn(self):
        self.__set_undo()
        self.goal = dn(self.goal)
        return False

    def auto(self) -> [str]:
        if not self.assumption():
            if self.goal is None:
                return ["assumption"]
            elif ans := self.auto():
                return ["assumption"] + ans
            else:
                self.undo()
        if not self.intro():
            if ans := self.auto():
                return ["intro"] + ans
            else:
                self.undo()
        if not self.split():
            if ans := self.auto():
                return ["split"] + ans
            else:
                self.undo()
        if not self.left():
            if ans := self.auto():
                return ["left"] + ans
            else:
                self.undo()
        if not self.right():
            if ans := self.auto():
                return ["right"] + ans
            else:
                self.undo()
        for i in range(len(self.variables)):
            if not self.apply(i):
                if ans := self.auto():
                    return [f"apply {i}"] + ans
                else:
                    self.undo()
            if not self.destruct(i):
                if ans := self.auto():
                    return [f"destruct {i}"] + ans
                else:
                    self.undo()
            for j in range(len(self.variables)):
                if not self.specialize(i, j):
                    if ans := self.auto():
                        return [f"specialize {i} {j}"] + ans
                    else:
                        self.undo()
        return []
