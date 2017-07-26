def partition(seq, func=bool):
    true_vals, false_vals = [], []
    def true_gen(_seq):
        while 1: 
            if true_vals:
                yield true_vals.pop(0)
            else:
                for item in _seq:
                    if func(item):
                        yield item
                        break
                    else:
                        false_vals.append(item)
                else:
                    break
    def false_gen(_seq):
        while 1:
            if false_vals:
                yield false_vals.pop(0)
            else:
                for item in _seq:
                    if not func(item):
                        yield item
                        break
                    else:
                        true_vals.append(item)
                else:
                    break
    it = iter(seq)
    return true_gen(it), false_gen(it)
