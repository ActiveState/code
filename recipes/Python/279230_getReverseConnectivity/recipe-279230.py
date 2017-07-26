#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def getReverseConnectivity(connectivity):
    """getReverseConnectivity(connectivity) -->
       resort connectivity dict with nodes as keys"""
    reverseConnectivity = {}
    for el, conn in connectivity.items():
        for node in conn:
            if node not in reverseConnectivity.keys():
                reverseConnectivity[node]=[el,]
            else:
                reverseConnectivity[node].append(el)
    return reverseConnectivity


>>> sc = {70: [156, 159, 158, 155], 69: [155, 158, 157, 154], 68: [153, 156, 155, 152], 67: [152, 155, 154, 151]}
>>> getReverseConnectivity(sc)
{159: [70], 158: [70, 69], 157: [69], 156: [70, 68], 155: [70, 69, 68, 67], 154: [69, 67], 153: [68], 152: [68, 67], 151: [67]}
