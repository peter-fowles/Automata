

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

class Operation:
    def __init__(self, read, pop, push):
        self.read = read
        self.pop = pop
        self.push = push

    def __str__(self) -> str:
        return f'read {self.read}, pop {self.pop}, push {self.push}'
        
    def __repr__(self):
        return f'read {self.read}, pop {self.pop}, push {self.push}'

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
        newStack = Stack()
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
        return str(self.__stack) + ', top = ' + str(self.top())
    
class Snapshot:
    def __init__(self, string, stack):
        self.string = string
        self.stack = stack
    
    def __eq__(self, other: object) -> bool:
        return self.string == other.string and self.stack == other.stack
    
    def __str__(self):
        return f'{self.string}, {self.stack}'
    
    def __repr__(self) -> str:
        return self.__str__()

class StackMachine:
    def __init__(self, G):
        self.grammar = G
        self.operations = set()

        for v in self.grammar.variables:
            if v in self.grammar.productions:
                for production in self.grammar.productions[v]:
                    self.operations.add(Operation(None, v, production))
        for a in self.grammar.alphabet:
            self.operations.add(Operation(a, a, None))
    
    def __repr__(self) -> str:
        s = ''
        for op in self.operations:
            s += f'{op}\n'
        return s
    
    def process(self, string):
        stack = Stack()
        stack.push(self.grammar.start_symbol)
        return self.__process(Snapshot(string, stack))

    def __process(self, start):
        queue = [start]
        seenStates = []
        while queue:
            curr = queue.pop(0)
            seenStates.append(curr)
            for op in self.operations: 
                if (op.read is None or curr.string and op.read == curr.string[0]) and op.pop == curr.stack.top():
                    nextStack = curr.stack.copy()
                    nextStack.pop()
                    nextString = curr.string
                    if op.push is not None:
                        for item in op.push[::-1]:
                            nextStack.push(item)
                    if op.read is not None:
                        nextString = curr.string[1:]
                    nextState = Snapshot(nextString, nextStack)
                    if nextState not in seenStates:
                        queue.append(nextState)
            if len(curr.string) == 0 and curr.stack.isEmpty():
                return True
        return False
            
        
if __name__ == '__main__':
    G = ContextFreeGrammar(V={'S'}, Sigma={'a', 'b'})
    G.addProduction('S', 'aSa')
    G.addProduction('S', 'bSb')
    G.addProduction('S', None)
    M = StackMachine(G)
    print(M.process('abaaba'))

            
        