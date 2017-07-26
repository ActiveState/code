import timeit,heapq,bisect,random,decimal
   
class actions:
    def __init__(self,data):
        self.data=data
        self.data_types=('heapq','bisect','list')
    def create(self,the_type):
        new_data=[]
        if the_type=='heapq':
            for i in Data: heapq.heappush(new_data,i)
            print len(new_data)
        elif the_type=='list':
            for i in Data: new_data.append(i)
        elif the_type=='bisect':
            for i in Data: bisect.insort(new_data,i)
        self.new_data=new_data
    def pop1(self,the_type):
        if the_type=='heapq':
            heapq.heappop(self.new_data)
        elif the_type=='list':
            self.new_data.sort(reverse=True)
            self.new_data.pop()
        elif the_type=='bisect':
            self.new_data.pop(0)
    def pop2(self,the_type):
        if the_type=='heapq':
            heapq.heappush(self.new_data,0)
            heapq.heappop(self.new_data)
        elif the_type=='list':
            self.new_data.append(0)
            self.new_data.sort()
            self.new_data.pop()
        elif the_type=='bisect':
            bisect.insort(self.new_data,0)
            self.new_data.pop(0)
    def show500(self,the_type):
        if the_type=='heapq':
            heapq.nlargest(500,self.new_data)
        elif the_type=='list' or 'bisect':      
                self.new_data[-500:]
#do rounding here w/decimal library to limit presence
#off odd floating point numbers
def rnd(flt):
    flt=round(flt,4)
    thread_context = decimal.getcontext()
    thread_context.prec=5
    dec_num=thread_context.create_decimal(str((flt)))
    return str(dec_num)


Results={}
Actions=['create','pop1','pop2','show500']
for num in (10000,100000,200000,1000000,):
    print 'at',num
    Data=[ random.randrange(1000000) for i in range(num) ]
    action_obj=actions(Data)
    for data_type in action_obj.data_types:
        Results[data_type]={}
        for action in Actions:
            specific_action=getattr(action_obj,action)
            begin=time.clock()
            specific_action(data_type)
            end=time.clock()-begin
            Results[data_type][action]=rnd(end)
    print '\t',
    for action in Actions: print action,'\t',
    print ''
    ref=0
    for data_type in Results:
        print data_type,'\t',
        for action in Actions:
            print Results[data_type][action],'\t',
        print ''
#######Results
at 10000
        create  pop1    pop2    show500
bisect  0.0782  0.0001  0.0001  0.0001
heapq   0.0101  0.0     0.0     0.0069
list    0.0061  0.0119  0.0013  0.0001
at 100000
        create  pop1    pop2    show500
bisect  10.994  0.0008  0.0013  0.0001
heapq   0.1156  0.0     0.0     0.0318
list    0.0968  0.1908  0.0577  0.0001
at 200000
        create  pop1    pop2    show500
bisect  78.837  0.0017  0.0046  0.0001
heapq   0.245   0.0     0.0     0.06
list    0.2039  0.4406  0.1402  0.0001
at 300000
        create  pop1    pop2    show500
bisect  201.39  0.0027  0.0065  0.0002
heapq   0.3438  0.0     0.0     0.0684
list    0.2888  0.7267  0.214   0.0001

at 1000000 #(skipping bisect)
        create  pop1    pop2    show500
heapq   1.4689  0.0004  0.0     0.1984
list    0.8342  3.1588  0.8904  0.0002
