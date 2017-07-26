def Name(**kw):
    assert len(kw)==1
    name, obj = kw.items()[0]
    obj.func_name = name
    return obj

def main():
    f = Name(CheckExists=lambda:os.path.exists(some_filename))
    print f

if __name__ == '__main__':
    main()
