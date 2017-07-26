from copy import copy

def mrange(min_values, max_values=None):
    '''
        Inputs: min_values, a list/tuple with the starting values
                    if not given, assumed to be zero
                max_values: a list/tuple with the ending values
        outputs: a tuple of values
    '''
    
    if not max_values:
        max_values = min_values
        min_values = [0 for i in max_values]
    indices_list = copy(min_values)

    #Yield the (0,0, ..,0) value
    yield tuple(indices_list)
    
    while(True):
        indices_list = updateIndices(indices_list, min_values, max_values)
        if indices_list:
            yield tuple(indices_list)
        else:
            break#We're back at the beginning
   
def updateIndices(indices_list, min_values, max_values):
    '''
        Update the list of indices
    '''
    for index in xrange(len(indices_list)-1, -1, -1):
        #If the indices equals the max values, the reset it and 
        #move onto the next value
        if not indices_list[index] == max_values[index] - 1:
            indices_list[index] += 1
            return indices_list
        else:
            indices_list[index] = min_values[index]
    return False        

#example

for i in mrange([2,2,1,2]):
    print i
(0, 0, 0, 0)
(0, 0, 0, 1)
(0, 1, 0, 0)
(0, 1, 0, 1)
(1, 0, 0, 0)
(1, 0, 0, 1)
(1, 1, 0, 0)
(1, 1, 0, 1)

#So the rather horrid
for i in range(1):
    for j in range(2):
        for k in range(3):
            for l in range(4):
                print i, j, k, l
#reduces to
for i, j, k, l in mrange([1,2,3,4]):
    print i, j, k, l
