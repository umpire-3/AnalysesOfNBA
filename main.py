from input import data
from automaton import Automaton

import analyser


automaton = Automaton(**data)
# print(data['TransitionRelation'])
# print(automaton._trans_relation)

L = analyser.get_omega_language(automaton)

for i, state in enumerate(automaton._states):
    print('State #{} = {}'.format(i, state))
print()
print('L(Buchi Automaton) =', L)
