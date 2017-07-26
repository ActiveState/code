def sort_list_of_dictionary(l, key, deep_copy=True):

    ''' sorts a list of dictionary based on a key value

        by Ritesh Nadhani, riteshn@gmail.com, 08/19/2008

        if deep_copy is True then it returns a new list otherwise it does a inline sorting

        tests:
            l = [
                {'key':'R', 'item1':'item1', 'item2':'item2'},
                {'key':'Z', 'item1':'item1', 'item2':'item2'},
                {'key':'A', 'item1':'item1', 'item2':'item2'},
                {'key':'B', 'item1':'item1', 'item2':'item2'},
            ]

            # deep_copy = True
            n = sort_list_of_dictionary(l, 'key')

            print "Sorted List ", n, " Original List ", l

            # deep_copy = False
            sort_list_of_dictionary(l, 'key', False)

            print "Sorted List ", l
    '''

    if deep_copy:
        result = copy.deepcopy(l)
        result.sort(lambda x,y:cmp(x[key],y[key]))
        return result
    else:
        l.sort(lambda x,y:cmp(x[key],y[key]))
