def prune(L, unique_items):
    """Remove all items in the 'unique_items' list from list L"""
    map(L.remove, unique_items)

def graft(L, unique_items):
    """Add all items in the list 'unique_items' from list L"""
    L.extend(unique_items)

def unique(L1, L2):
    """Return a list containing all items in 'L1' that are not in 'L2'"""
    return [item for item in L1 if item not in L2]

# Sample code demonstratiing use
if __name__ == "__main__":

    # We start with two lists, and we want list1 to
    # be synchronized with list2
    list1 = ["a", "b", "c", "e", "f", "d"]
    list2 = ["a", "b", "f", "g"]

    # Prune extra items out of list1
    prune(list1, unique(list1, list2))

    # Graft any extra items from list2 into list1
    graft(list1, unique(list2, list1))

    print "list1 =", list1
    print "list2 =", list2
