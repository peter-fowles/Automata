

class ContextFreeGrammar:
    def __init__(self, V=set(), Sigma=set([None]), S='S', P={}):
        self.variables = V
        self.alphabet = Sigma
        self.start_symbol = S
        self.productions = P

    def addProduction(self, v, production):
        if v not in self.variables:
            raise ValueError
        if production is not None:
            for s in production:
                if s not in self.variables and s not in self.alphabet:
                    raise ValueError
        if v not in self.productions:
            self.productions[v] = []
        self.productions[v].append(production)

    def __repr__(self) -> str:
        s = f'V = {self.variables}\n'
        s += f'Sigma = {self.alphabet}\n'
        s += f'S = {self.start_symbol}\n'
        s += 'P = {\n'
        for p in self.productions:
            s += f'    {p} -> {self.productions[p]}\n'
        s += '}'
        return s

    def produces(self, string):
        pass


class StackMachine:
    def __init__(self, G):
        self.grammar = G
        self.operations = set()

        for v in self.grammar.variables:
            if v in self.grammar.productions:
                for production in self.grammar.productions[v]:
                    self.operations.add(self.Operation(None, v, production))
        for a in self.grammar.alphabet:
            self.operations.add(self.Operation(a, a, None))

    def __performOperation(self, op, state):
        nextStack = state.stack.copy()
        nextStack.pop()
        nextString = state.string
        if op.push is not None:
            for item in op.push[::-1]:
                nextStack.push(item)
        if op.read is not None:
            nextString = state.string[1:]
        return self.Snapshot(nextString, nextStack)

    
    def process(self, string, showFinals=False):
        stack = self.Stack()
        stack.push(self.grammar.start_symbol)
        results = self.__process(self.StateList([self.Snapshot(string, stack)]))
        if showFinals:
            for result in results:
                print(result)
        return bool(results)

    def __process(self, start):
        queue = [start]
        seenStates = set()
        finalSolutionPaths = []
        while queue:
            stateList = queue.pop(0)
            curr = stateList.curr()
            seenStates.add(curr)
            for op in self.operations: 
                if (op.read is None or curr.string and op.read == curr.string[0]) and op.pop == curr.stack.top():
                    nextState = self.__performOperation(op, curr)
                    nextStateList = stateList.copy()
                    nextStateList.add(nextState)
                    if nextState not in seenStates:
                        queue.append(nextStateList)
            if len(curr.string) == 0 and curr.stack.isEmpty():
                finalSolutionPaths.append(stateList)
        return finalSolutionPaths
    
    def __repr__(self) -> str:
        s = ''
        for op in self.operations:
            s += f'{op}\n'
        return s

    class Operation:
        def __init__(self, read, pop, push):
            self.read = read
            self.pop = pop
            self.push = push

        def __str__(self) -> str:
            return f'read {self.read}, pop {self.pop}, push {self.push}'
            
        def __repr__(self):
            return f'read {self.read}, pop {self.pop}, push {self.push}'
        
    class StateList:
        def __init__(self, states=[]):
            self.__states = []
            for state in states:
                self.__states.append(state)
        
        def copy(self):
            newStates = type(self)()
            for state in self.__states:
                newStates.add(state)
            return newStates
        
        def add(self, state):
            self.__states.append(state)
        
        def curr(self):
            if not self.__states:
                return None
            return self.__states[-1]
        
        def __repr__(self) -> str:
            s = ''
            for state in self.__states[:-1]:
                s += str(state)
                s += ' -> '
            s += str(self.curr())
            return s

    class Stack:
        def __init__(self):
            self.__stack = []

        def show(self):
            return self.__stack
        
        def push(self, item):
            if item is not None:
                self.__stack.append(item)

        def pop(self):
            return self.__stack.pop()
        
        def copy(self):
            newStack = type(self)()
            for item in self.__stack:
                newStack.push(item)
            return newStack
        
        def top(self):
            if len(self.__stack) == 0:
                return None
            return self.__stack[-1]
        
        def isEmpty(self):
            return len(self.__stack) == 0
        
        def clear(self):
            self.__stack = []
        
        def __eq__(self, other: object) -> bool:
            if len(self.__stack) != len(other.__stack):
                return False
            result = True
            for i in range(len(self.__stack)):
                result &= self.__stack[i] == other.__stack[i]
            return result

        def __str__(self):
            return str(self.__stack)
    
    class Snapshot:
        def __init__(self, string, stack):
            self.string = string
            self.stack = stack
        
        def __eq__(self, other: object) -> bool:
            return self.string == other.string and self.stack == other.stack
        
        def __str__(self):
            return f'("{self.string}", {self.stack})'
        
        def __repr__(self) -> str:
            return self.__str__()
        
        def __hash__(self) -> int:
            return str(self).__hash__()
        
if __name__ == '__main__':
    G = ContextFreeGrammar(V={'S', 'B'}, Sigma={'a', 'b'})
    G.addProduction('S', 'aS')
    G.addProduction('S', 'B')
    G.addProduction('S', None)
    G.addProduction('B', None)
    G.addProduction('B', 'bB')
    M = StackMachine(G)
    print('Grammar:')
    print(G)
    print('Machine:')
    print(M)
    s = 'aabbbbbbb'
    result = M.process(s, showFinals=True)
    print('\"' + s + '\" ' + ('is in L(M)' if result else 'is not in L(M)'))

            
        