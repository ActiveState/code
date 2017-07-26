###############################################
#
# sqlSortable Class - this class supports sorting of objects using 
#                     the same terms as used when specifying a sort in SQL
#   Andrew M. Henshaw 8/15/01


class sqlSortable:
    def __init__(self, **args):
        self.__dict__.update(args)

    def setSort(self, sortOrder):
        self.sortFields = []
        for text in sortOrder:
            sortBy, direction = (text+' ').split(' ', 1)
            self.sortFields.append((sortBy, direction[0:4].lower() == 'desc'))
    
    def __repr__(self):
        return repr([getattr(self, x) for x, reverse in self.sortFields])
        
    def __cmp__(self, other):
        myFields    = []
        otherFields = []
        for sortBy, reverse in self.sortFields:
            myField, otherField = getattr(self, sortBy), getattr(other, sortBy)
            if reverse:
                myField, otherField = otherField, myField
            myFields.append(myField)
            otherFields.append(otherField)
        return cmp(myFields, otherFields)



def testSqlSortable():
    data = [('Premier', 'Stealth U-11'),('Premier', 'Stealth U-10'),('Premier', 'Stealth U-12'),
            ('Co-ed',   'Cyclones'),    ('Co-ed',   'Lightning'),   ('Co-ed',   'Dolphins'),
            ('Girls',   'Dynamos'),     ('Girls',   'Tigers'),      ('Girls',   'Dolphins')]

    testList = [sqlSortable(program=program, name=name) for program, name in data]

    tests = [['program DESC', 'name'],
             ['name desc', 'program asc']]

    for sortBy in tests:
        print '#### Test basic sorting ###', sortBy
        for sortable in testList:
            sortable.setSort(sortBy)
        testList.sort()
        for item in testList:
            print item
    print '#### Test modification of attributes ###', sortBy
    assert testList[4].name == 'Lightning'
    testList[4].name = 'ZZ 1st name'
    testList.sort()
    for item in testList:
        print item
    

if __name__ == '__main__':
    testSqlSortable()
