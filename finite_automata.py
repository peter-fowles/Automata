
class FA:
    def __init__(self, Q:set, Sigma:set, delta:dict, q_0:str, F:set) -> None:
        self.states = Q
        self.alphabet = Sigma
        self.transitions = delta
        self.start = q_0
        self.final_states = F
    
    def addTransition(self, fn:tuple, end):
        if fn not in self.transitions:
            self.transitions[fn] = set()
        self.transitions[fn].add(end)

    def __repr__(self) -> str:
        return \
        f'Q = {{{','.join([str(item) for item in self.states])}}}\nSigma = {{{','.join(self.alphabet)}}}\ndelta = {{\n\t{"\n\t".join(["d(%s) = %s" % (str(key), str(value)) for (key, value) in self.transitions.items()])}\n\t}}\nq_0 = {str(self.start)}\nF = {{{",".join([str(state) for state in self.final_states])}}}'.replace('\'', '').replace(',)',')')
    
    def processString(self, string:str) -> bool:
        curr_states = [self.start]
        for char in string:
            next_states = []
            for state in curr_states:
                for item in self.transitions[(state, char)]:
                    next_states.append(item)
            curr_states = [item for item in next_states]
        for state in curr_states:
            if state in self.final_states:
                return True
        return False
    
    def isDFA(self) -> bool:
        result = True
        for state in self.states:
            for char in self.alphabet:
                result &= (state, char) in self.transitions and len(self.transitions[(state, char)]) == 1
        return result

    def convertToDFA(self):
        new_start = tuple([self.start])
        queue = [new_start]
        new_states = set()
        new_transitions = dict()
        while queue:
            q_next = queue.pop(0)
            if q_next in new_states:
                continue
            for char in self.alphabet:
                next_transition = set()
                for state in q_next:
                    if (state, char) in self.transitions:
                        for d in self.transitions[(state, char)]:
                            next_transition.add(d)
                next_transition = list(next_transition)
                next_transition.sort()
                next_transition = tuple(next_transition)
                new_transitions[(q_next, char)] = set([next_transition])
                queue.append(next_transition)
                new_states.add(q_next)
        new_final_states = set()
        for state in new_states:
            for final in self.final_states:
                if final in state:
                    new_final_states.add(state)
        return FA(
            Q=new_states,
            Sigma=set([char for char in self.alphabet]),
            delta=new_transitions,
            q_0=new_start,
            F=new_final_states
        )