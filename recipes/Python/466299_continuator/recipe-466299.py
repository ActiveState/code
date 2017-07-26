from collections import deque

class continuator:
    def __init__(self, gen):
        self.stack = deque([gen])
    def __iter__(self):
        return self
    def next(self):
        try:
            gen = self.stack[-1]
        except IndexError:
            raise StopIteration
        try:
            ret_val = gen.next()
            if hasattr(ret_val, 'gi_frame'):
                self.stack.append(ret_val)
                return self.next()
            else:
                return ret_val
        except StopIteration:
            try:
                self.stack.pop()
                return self.next()
            except IndexError:
                raise StopIteration

#### EXAMPLE ###########################################################

def gen_abcd():
    for text in ['aaa','bbb','ccc','ddd']:
        yield text

def gen_efgh():
    for text in ['eee','fff','ggg','hhh']:
        yield text

def gen_ijkl():
    yield "iii"
    yield gen_jk()
    yield 'lll'

def gen_jk():
    yield "jjj"
    yield gen_k()

def gen_k():
    yield "kkk" 

def gen_all():
    yield gen_abcd()
    yield gen_efgh()
    yield gen_ijkl()

for text in continuator(gen_all()):
    print text
