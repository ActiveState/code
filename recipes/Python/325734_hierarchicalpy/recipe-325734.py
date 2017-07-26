messages = dict()  #   {index : [niveau,index_parent,message]
filiation = dict() #   {index_parent:[liste_des_fils]}

class message:
    def __init__(self,idx,idx_parent,message):
	self.idx = idx
	self.idx_parent = idx_parent
	self.message = message
	self.level = 0
	self.ajout_message()

    def ajout_message(self):
	if self.idx_parent:
	    self.level = messages[self.idx_parent][0] + 1
	messages[self.idx] = [self.level,self.idx_parent,self.message]
	self.update_filiation()
		    
    def update_filiation(self):
	if self.idx_parent:
	    parent = self.idx_parent
	    if filiation.has_key(parent):
		filiation[parent].append(self.idx)
	    else:
		filiation[parent]=[self.idx]
	else:
	    filiation[self.idx]=[]

def liste_rep(num):
    sep = ' |-'
    try:
	mess = messages[num][2]
	level = messages[num][0]
	if level :
	    print '  |'*(level),sep,mess,'('+ `num`+')'
	else :
	    print num,mess
    except:
	pass
    if filiation.has_key(num):
	for i in filiation[num]:
	    liste_rep(i)

def liste_all():
    for i in filiation.keys():
	if messages[i][1] == None: #pas de parent
	    liste_rep(i)

	    
					   
if __name__ == '__main__':
    import pprint
    m = message(1,None,'first message')
    m = message(2,1,'response to the first message')
    m = message(3,1,'response to the first message')
    m = message(4,2,'response to the second message')
    m = message(5,None,'fifth message')
    m = message(6,2,'response to the second message')
    m = message(7,1,'response to the first message')
    m = message(8,6,'response to the sixth message')
    m = message(9,5,'response to the fifth message')
    m = message(10,None,'tenth message')
    m = message(11,None,'eleventh message')
    print "Filiation Dictionnary{index_parent:[list_of_childs]}:"
    pprint.pprint(filiation)
    print
    print "Messages Dictionary {message_number : [level,index_parent,content]}:"
    pprint.pprint(messages)
    print
    print "Displaying the tree messages"
    liste_all()
