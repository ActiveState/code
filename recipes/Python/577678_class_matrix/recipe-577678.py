class Point():
    def __init__(self,x,y,dim):
        self.x = x
        self.y = y
        self.dim = dim
        
class matrix(object):
    def __init__(self,mat):
        self.mat = mat
        self.row = len(mat)
        self.col = len(mat[0])
        self._matRes = []
        self.__s = ''
        
    def __str__(self):
        for i in range(self.row):
        	self.__s += '\n'
        	for j in range(self.col):
        		self.__s += '%g\t' %(self.mat[i][j])
        return self.__s
    
    
    def __mul__(self,other):
        if isinstance(other,int) or isinstance(other,float):
            for i in range(self.row):
                for j in range(self.col):
                    self.mat[i][j] *= other
            return matrix(self.mat)
                
        if self.col != other.row: return 'The number of columns of the first matrix must be equal to the number of rows of the second.'
        self._matRes = [[0 for r in range(other.col)] for c in range(self.row)]
        for i in range(self.row):
            for j in range(other.col):
                for k in range(other.row):
                    self._matRes[i][j] += self.mat[i][k] * other.mat[k][j]               
        return matrix(self._matRes)
    
    def __add__(self,other):
        if not (self.row == other.row) and (self.col == other.col): return 'The number of col is not equal to the number of row'
        self._matRes = [[0 for r in range(self.col)] for c in range(self.row)]
        for i in range(self.row):
            for j in range(self.col):
                self._matRes[i][j] += self.mat[i][j] + other.mat[i][j]
        return matrix(self._matRes)
        
    def __pow__(self,other):
    	if not isinstance(other,int): return 'only int'
    	if other == 0: return 'Prime matrix'
    	if other < 0: return 'only int'
    	for i in range(1,other+1):
    		if i != other:
    			self.__s += 'matrix(self.mat)*'
    		else:
    			self.__s += 'matrix(self.mat)'
    	return eval(self.__s)

    def det(self, point):
    	M = point.dim - 1
    	if len(self.mat) == 2 :
            return (int(self.mat[0][0]) * int(self.mat[1][1])) - (int(self.mat[0][1]) * int(self.mat[1][0]))

    	s = 0
    	for row in range(1, point.dim+1):
        	copyli = []
        	for i in range(1,len(li)):
                    copyli1 = []
            	for j in range(len(li)) :
                	if (row - 1) != j :
                		copyli1.append(li[i][j])
            	copyli.append(copyli1)
                
        	s += (-1) ** (1 + row) * int(li[0][row-1]) * det(copyli, Point(1, row, M))
    	return s
       
		
		
		
def inverse(self):
	pass
    
    
    
print matrix.det(matrix([[1,2],[2,3]]))
   
#print (matrix([[15,24,33],[21,-34,25]]) * matrix([[15,24],[21,-34],[1,3]]))* matrix([[1,2],[2,3]])

#print (matrix([[1,2,12,33,2,2],[1,2,3,22,1,3],[1,21,3,4,2,4],[111,31,34,2,12,1],[2,33,122,1,3,3],[1,19,90,6,2,4]]))**10
#print ( matrix([[1,2],[2,3]]) * matrix([[1,2],[2,3]])) + matrix([[1,2],[2,3]])
