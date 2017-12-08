class Automaton:

    @staticmethod
    def _build_relation(data):
        relation = dict()
        for (s1, a, s2) in data:
            try:
                value = relation[(s1, s2)]
                value.append(a)
            except KeyError:
                relation[(s1, s2)] = [a]
        return relation

    def _build_state_map(self, data):
        self._states = list(data)
        self._name_to_state = {}

        for state, name in enumerate(self._states):
            self._name_to_state[name] = state

    def __init__(self, **kwargs):
        states = kwargs['States']
        init_states = kwargs['InitialStates']
        final_states = kwargs['FinalStates']
        E = kwargs['Alphabet']
        relation = kwargs['TransitionRelation']

        self._build_state_map(states)
        self._init_states = init_states
        self._final_states = final_states
        self._E = E
        self._trans_relation = self._build_relation(relation)

    def size(self):
        return len(self._states)

    def state(self, name):
        try:
            return self._name_to_state[name]
        except KeyError:
            raise

    def get_transitions(self, s1, s2):
        try:
            return self._trans_relation[
                self._states[s1],
                self._states[s2]
            ]
        except KeyError:
            return []

    def is_initial(self, state):
        return self._states[state] in self._init_states

    def is_final(self, state):
        return self._states[state] in self._final_states

    def get_seq_by(self, s1, s2):
        n1 = self.state(s1)
        n2 = self.state(s2)
        seq = [n1]
        for i in range(self.size()):
            if i not in (n1, n2):
                seq.append(i)
        seq.append(n2)
        return seq
