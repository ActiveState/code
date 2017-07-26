# nice and clean closure notation
def get_counter_neat():
    def f():
        f.x += 1
        return f.x
    f.x = 0
    return f

# traditional, not_so_neat closure notation
def get_counter_traditional():
    x = [0]
    def f():
        x[0] += 1
        return x[0]
    return f

#### EXAMPLE ###########################################################

cnt_a = get_counter_neat()
cnt_b = get_counter_neat()

print cnt_a()   # >>> 1
print cnt_a()   # >>> 2
print cnt_a()   # >>> 3
print cnt_b()   # >>> 1
print cnt_a()   # >>> 4
print cnt_b()   # >>> 2
print cnt_b()   # >>> 3
