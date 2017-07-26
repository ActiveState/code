import argparse

# this function can be anywhere
def get_list_of_local_callables():
    """Generate and return the list of the local callables
    """
    from inspect import stack
    caller_locals = stack()[1][0].f_locals
    loc_callables = dict((k, v) for k, v in caller_locals.items()
                         if callable(v))

    return loc_callables


# and we can use it simply with
def parse_arguments(actions):
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=actions)
    return parser.parse_args()

def main():
    def func1():
        pass

    def func2():
        pass

    loc_funs = get_list_of_local_callables()
    ns = parse_arguments(loc_funs.keys())

    loc_funs[ns.action]()

if __name__ == '__main__':
    main()
