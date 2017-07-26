class nloop:
    def __init__(self,*list):
        self.list = list
        self.memo_array = [None] * len(list)
        self.iter_list = []
        exec(self.n_combo(list))
    def __getitem__(self,index):
        return self.iter_list[index]

    def n_combo(self,lists):
        zipped = zip(list(range(len(lists))), lists)
        zipdex = map((lambda x: x[0]), zipped)
        str = "for"
        cmma = ''
        fora = ''
        for z in zipdex:
            cmma = cmma + ', ' + 'i%s' % z
        cmma = cmma[1:]
        i = 0
        for z in zipdex:
            fora = fora + 'for ' + 'i%s' % z + ' in self.list[%s] ' % i
            i = i + 1
        str = str + cmma + ' in [(' + cmma + ') ' + fora + ']:'

        cmd = "self.iter_list.append((" + cmma + "))"
        return str  + cmd


if __name__ == '__main__':
    for tup in nloop(list("abcdef"),
                     list(range(1,50)),
                     list("hijklmno"),
                     list(range(1,7))):
        print tup

###########################################

class nloop:
    def __init__(self,*varg):
        self.list = list(varg)
        self.iter_list = []

        self.memo = [None] * len(self.list)
        if len(self.list):
            self.n_iter(0, self.list)

    def __getitem__(self,index):
        return self.iter_list[index]

    def n_iter(self,index,stack):
        x = stack[index]
        for i in x:
            self.memo[index] = i
            if index == len(stack) - 1:
                self.iter_list.append(tuple(self.memo))
            else:
                self.n_iter(index + 1, stack)
                

if __name__ == '__main__':
    for tup in nloop(list("abcdef"),
                     list(range(1,50)),
                     list("hijklmno"),
                     list(range(1,7))):
        print tup
