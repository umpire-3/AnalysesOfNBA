import expression


def get_language(automaton, state_name):
    B = []
    for i in range(automaton.size()):
        if automaton.is_initial(i):
            B.append(expression.Epsilon())
        else:
            B.append(None)

    A = []
    for i in range(automaton.size()):
        _A = []
        for j in range(automaton.size()):
            transitions = automaton.get_transitions(j, i)
            if len(transitions) > 0:
                exp = expression.Union.from_terminal_seq(transitions)
                _A.append(exp)
            else:
                _A.append(None)
        A.append(_A)

    state = automaton.state(state_name)
    states = list(range(automaton.size()))
    seq = states[state:] + states[:state]
    print('Seqqq ====', ['{}({})'.format(s, automaton._states[s]) for s in seq])

    print('Sistema =')
    for i, (b, a_i) in enumerate(zip(B, A)):
        print('S({}) = '.format(automaton._states[i]), end='')
        row = ['S({}){}'.format(automaton._states[j], a) for j, a in enumerate(a_i) if a]
        if b:
            row = ['{}'.format(b)] + row
        print(' + '.join(row))
    print()

    while len(seq) != 0:
        n = seq.pop()
        if A[n][n]:
            if B[n]:
                B[n] = B[n].concat(A[n][n].iterate())
            for j in seq:
                if A[n][j]:
                    A[n][j] = A[n][j].concat(A[n][n].iterate())
        for i in seq:
            if A[i][n]:
                if B[n]:
                    if B[i]:
                        B[i] = B[i] + B[n].concat(A[i][n])
                    else:
                        B[i] = B[n].concat(A[i][n])
                for j in seq:
                    if A[n][j]:
                        if A[i][j]:
                            A[i][j] = A[i][j] + A[n][j].concat(A[i][n])
                        else:
                            A[i][j] = A[n][j].concat(A[i][n])

    return B[state]


def get_omega_language(automaton):
    final_languages = []

    for state in automaton._final_states:
        language = get_language(automaton, state)
        if isinstance(language, expression.Concat):
            left, right = language.operands
            if isinstance(right, expression.Iteration):
                final_languages.append(left.concat(right.operand.omega_iterate()))

    if len(final_languages) == 0:
        return None

    return expression.Union(*final_languages)
