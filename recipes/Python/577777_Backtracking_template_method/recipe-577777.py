def backtracking(choice_points, choices, assignable):
    """
    Template method
    choice_points: is a list of the choice points. Each of them will be assigned to a single choice for
          each solution.
    choices: is a list of choices.
    assignable: is a function that declare if a choice is assignable to a choice point. 
          It needs three arguments:
               def assignable(choice, choice_points, solutions):
          In particular, solutions store the assignments of the previous choice points.
          It seems like that {cp0:c0, cp1:c1, ...} where cpI is a choice point and cI is a choice.
    """
    
    N = len(choices)
    M = len(choice_points)
    
    # solutions is the dict that has for each choice point (key) a choice (value)
    solutions = {}
    
    cp=0
    c=0
    backtrack=False
    end=False
        
    while(not end):
        #forward
        while(  not backtrack ):
            if( assignable( cp, c, solutions ) ):
                solutions[cp] = c
                if( cp==M-1):
                    yield {choice_points[k]:choices[v] for k,v in solutions.iteritems()}
                    del solutions[cp]
                    if not c==N-1:
                        c+=1
                    else:
                        backtrack = True
                else:
                    cp+=1
                    c=0
            elif( c!=N-1):
                c+=1
            else:
                backtrack=True

        #backward
        end=(cp==0)
        while( backtrack and not end ):
            cp-=1
            c=solutions.pop(cp)
            if( not c==N-1 ):
                c+=1
                backtrack=False;
            elif( cp==0 ):
                end=True

            
            
if __name__=='__main__':
    
    
    ############## 4 Colors Problem #############
    neighbors = [set(), set(),set(),set(),set()]
    neighbors[0].add(1)
    neighbors[0].add(2)
    neighbors[1].add(2)
    neighbors[1].add(3)
    neighbors[1].add(0)
    neighbors[2].add(0)
    neighbors[2].add(1)
    neighbors[2].add(4)
    neighbors[3].add(1)
    neighbors[3].add(4)
    neighbors[4].add(2)
    neighbors[4].add(3)


    nations = ['Italy','Spain','France','Germany','England']
    colors = ['Yellow','Red','Blue','Black']
    
    def assignable4Colors(nation, color, solutions):
        """
        It's assignable a color to a nation if it's empty the intersection between neighbors of nation
        and the nations of the same color in solutions.
        """
        sameColor = set([n for n,c in solutions.iteritems() if c==color ])
        return neighbors[nation].isdisjoint(sameColor)
    
    
    for s in backtracking(nations, colors, assignable4Colors):
        print s
        
        
    ############## 8 Queens Problem ###############    
    rows = ['1', '2', '3', '4', '5', '6', '7', '8']
    columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    
    def assignable8Queens(row, column, solutions):
        for r, c in solutions.iteritems():
            if c == column:
                return False
            elif r-c == row-column:
                return False
            elif r+c == row+column:
                return False
        return True 
    
    for s in backtracking(rows, columns, assignable8Queens):
        print s
    
    
