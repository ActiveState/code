def pascals_triangle(n):
    '''
    Pascal's triangle:

    for x in pascals_triangle(5):
        print('{0:^16}'.format(x))

          [1]       
         [1, 1]     
       [1, 2, 1]    
      [1, 3, 3, 1]  
    [1, 4, 6, 4, 1]
    '''
    x=[[1]]
    for i in range(n-1):
        x.append([sum(i) for i in zip([0]+x[-1],x[-1]+[0])])
    return x
