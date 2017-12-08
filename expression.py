class Expression:
    Priority = None

    def __init__(self, *operands):
        self.operands = operands

    def __add__(self, other):
        if isinstance(other, Expression):
            return Union(self, other)
        else:
            return Union(self, Terminal(other))

    def concat(self, other):
        if isinstance(other, Epsilon):
            return self
        elif isinstance(other, Expression):
            return Concat(self, other)
        else:
            return Concat(self, Terminal(other))

    def iterate(self):
        return Iteration(self)

    def omega_iterate(self):
        return OmegaIteration(self)

    def _stringify_operands(self):
        operands = []
        for operand in self.operands:
            if operand.Priority < self.Priority:
                operands.append('({})'.format(str(operand)))
            else:
                operands.append(str(operand))
        return operands

    def __str__(self):
        pass

    def __repr__(self):
        return str(self)


class UnaryExpression(Expression):
    @property
    def operand(self):
        return self.operands[0]


class AssociativeExpression(Expression):
    @classmethod
    def from_terminal_seq(cls, seq):
        if len(seq) == 1:
            return Terminal(seq[0])
        return cls(*(Terminal(terminal) for terminal in seq))


class Terminal(UnaryExpression):
    Priority = 3

    def __str__(self):
        return self.operands[0]


class Union(AssociativeExpression):
    Priority = 0

    def __str__(self):
        return ' + '.join(operand for operand in self._stringify_operands())


class Concat(AssociativeExpression):
    Priority = 1

    def __str__(self):
        return ''.join(operand for operand in self._stringify_operands())


class Iteration(UnaryExpression):
    Priority = 2

    def __str__(self):
        return '{}*'.format(self._stringify_operands()[0])


class OmegaIteration(UnaryExpression):
    Priority = 2

    def __str__(self):
        return '{}\N{GREEK SMALL LETTER OMEGA}'.format(self._stringify_operands()[0])


class Epsilon(Terminal):
    def __init__(self):
        super().__init__('\N{GREEK SMALL LETTER EPSILON}')

    def concat(self, other):
        return other

    def iterate(self):
        return self

    def omega_iterate(self):
        return self
