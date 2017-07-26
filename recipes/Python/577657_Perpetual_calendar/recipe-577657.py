'''Program made by riddle to represent the so-called "perpetual calendar"
( http://www.evilmadscientist.com/article.php/perpetualcalendar )
BTW: if you don't know what year it is, you're just fucked.
'''
from datetime import date

daysofweek = ("Sunday","Monday","Tuesday",
              "Wednesday","Thursday","Friday","Saturday")

months = ("January","February","March","April","May","June","July","August",
          "September","October","November","December")

today = (date.today().isoweekday()+1,
         date.today().isoformat()[5:7],
         date.today().isoformat()[8:])

class Matrix(object):
    '''Matrix type is initialized with two args: # of columns and # of rows'''
    def __init__(self, cols, rows):
        self.cols = cols; self.rows = rows; self.matrix = []
        for i in range(rows):
            ea_row = []
            for j in range(cols): ea_row.append(0)
            self.matrix.append(ea_row)

    def setitem(self, col, row, x):
        self.matrix[col-1][row-1] = x
    
    def getitem(self, col, row):
        return self.matrix[col-1][row-1]
    
    def __repr__(self):
        outStr = ""
        for i in range(self.rows): outStr += '%s\n' % (self.matrix[i])
        return outStr

      
def d2b(n):
    '''Returns the base 2 value of non-negative int n (base 10) as a list'''
    binStr= ''
    if n < 0: raise ValueError("number must be non-negative")
    if n == 0: return '0'
    while n > 0: binStr = str(n%2)+binStr; n = n>>1
    return list(binStr)

    
def binarycalendar(dweek=today[0], mnth=today[1], dmonth=today[2]):
    '''Returns, as a Matrix, a binary representations of
   the day of the week, the month, and the day of month.
   
   Keyword arguments:
   dweek -- day of the week; defaults to today
   mnth -- month; defaults to the current month
   dmonth -- day of the month; defaults to today
   
   '''
    bcal = (d2b(dweek),d2b(int(mnth)),d2b(int(dmonth)))
    bcmatrix= Matrix(3,5)
    for x in range(3):
        if len(bcal[x])<5:
            for y in range(5-len(bcal[x])): bcal[x].insert(0,'0')
        for y in range(5): bcmatrix.setitem(y+1,x+1,bcal[x][y])
    bcmatrix.setitem(1,1,' ')
    bcmatrix.setitem(2,1,' ')
    bcmatrix.setitem(1,2,' ')
    return bcmatrix
   

if __name__ == '__main__':
    print(str(binarycalendar().__repr__()).replace('[','')
          .replace('\'','').replace(',','').replace(']',''))
    print("%s, %s %s" %
          (daysofweek[int(today[0]-1)], months[int(today[1])-1], today[2]))
