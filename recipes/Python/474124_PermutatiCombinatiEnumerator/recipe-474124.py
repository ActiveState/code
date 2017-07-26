def CombinationEnumerator(listObj, selection) :
    class CombEnum(object) :
        def __init__(self, listObj, selection) :
            assert selection <= len(listObj)
            self.items = listObj
            self.route = ([True, ]*selection) + [False, ]*(len(listObj)-selection)
            self.selection = selection
        def value(self) :
            result = [ val for flag, val in zip(self.route, self.items) if flag ]
            return result
        def next(self) :
            try :
                while self.route[-1] :
                    self.route.pop()
                while not self.route[-1] :
                    self.route.pop()
            except :
                return False

            self.route[-1] = False

            count = self.route.count(True)
            self.route.extend( (self.selection - count) * [True,] )
            padding = len(self.items) - len(self.route)
            self.route.extend( padding * [False, ])
            return True

    if selection == 0 :
        yield []
        return

    rotor = CombEnum(listObj, selection)
    yield rotor.value()
    while rotor.next() :
        yield rotor.value()

def PermutationEnumerator(choice, selection = None) :
    if not selection :
        selection = len(choice)
    class Rotor(object) :
        def __init__(self, choice, selection, parent = None) :
            assert len(choice) >= selection 
            self.selection = selection
            self.parent = parent
            self.choice = choice
            self.cursor  = 0
            if selection == 1 :
                self.child = None
            else :
                self._spawn_child()
        def value(self) :
            if self.child :
                result = self.child.value()
                result.append(self.choice[self.cursor])
                return result
            else :
                return [ self.choice[self.cursor], ]
        def _spawn_child(self) :
            assert self.selection >= 2
            cursor = self.cursor
            child_choice = self.choice[:cursor] + self.choice[cursor + 1:]
            self.child = Rotor(child_choice, self.selection -1,  self)
        def next(self) :
            result = False
            if self.child :
                result = self.child.next()

            if result :
                return result
            else :
                self.cursor += 1
                if self.cursor == len(self.choice) :
                    return False
                else :
                    if self.child :
                        self._spawn_child()
                    return True
                
    rotor = Rotor(choice, selection)
    yield rotor.value()
    while rotor.next() :
        yield rotor.value()

if __name__ == "__main__" : 
    items = [ 'a', 'b', 'c']
    for algo in (CombinationEnumerator, PermutationEnumerator) :
        for selection in range(1, 4) :
            print algo.__name__
            print items
            print selection
            enum = algo(items, selection)
            for i in enum :
                print i
            print "\n\n\n"
