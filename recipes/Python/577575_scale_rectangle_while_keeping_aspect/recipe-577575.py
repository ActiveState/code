def scale(w, h, x, y, maximum=True):
        nw = y * w / h
        nh = x * h / w
        if maximum ^ (nw >= x):
                return nw or 1, y
        return x, nh or 1
