from collections import deque

import random

'''
    Example below replicates 
    
    +75 MSFT 25.10
    +50 MSFT 25.12
    -100 MSFT 25.22
    
    Realized P&L = 75 * (25.22 - 25.10) + 25 * (25.22 - 25.12) = $ 11.50
    
    A Trade is split into a set of unit positions that are then dequeued on FIFO basis as part of Sell.

'''

number_of_sell_trades = 1000
max_sell_quentity = 5
min_sell_price = 23.00
max_sell_price = 27.00

class TradeManager():        

    def __init__(self):
        # FIFO queue that we can use to enqueue unit buys and
        # dequeue unit sells.
        self.fifo = deque()
        self.profit = []

    def __repr__(self):
        return 'position size: %d'%(len(self.fifo))
        
    def execute_with_total_pnl(self, direction, quantity, price):            
        #print direction, quantity, price, 'position size', len(self.fifo)
        
        if len(self.fifo) == 0:
            return 0
        
        if 'Sell' in (direction):            
            if len(self.fifo) >= quantity:                
                return sum([(price - fill.price) for fill in tm.execute(direction, quantity, price)])                
            else:
                return 0                
        else:
            return [tm.execute(direction, quantity, price)]           
            
    def execute(self, direction, quantity, price):        
        #print direction, quantity, price, 'position size', len(self.fifo)
        if direction in ('Buy'):            
            for i, fill in Trade(direction, quantity, price):                
                self.fifo.appendleft(fill)            
                yield fill
        elif direction in ('Sell'):
            for i, fill in Trade(direction, quantity, price):                
                yield self.fifo.pop()        

class Fill():    
        def __init__(self, price):
            self.price = price
            self.quantity = 1

class Trade():            
    def __init__(self, direction, quantity, price):
        self.direction = direction
        self.quantity = quantity
        self.price = price
        self.i = 0 
        
    def __iter__(self):
        return self
    
    def next(self):
        if self.i < self.quantity:
            i = self.i
            self.i += 1
            return i, Fill(self.price)
        else:
            raise StopIteration()
            
# create a TradeManager
tm = TradeManager()

# generate some buys
a = [i for i in tm.execute('Buy', 75, 25.10)]    
a = [i for i in tm.execute('Buy', 50, 25.12)]  

# generate sell
pnl = np.cumsum(tm.execute_with_total_pnl('Sell', 100, 25.22))

# how much did we make
print 'total pnl', pnl[-1:]

# try something more involved.
tm = TradeManager()
pnl_ending = []

# run n simulations 
for step in range(0,50):
    a = [i for i in tm.execute('Buy', 75000, 25)]    
    pnl = np.cumsum([tm.execute_with_total_pnl('Sell', quantity, random.uniform(min_sell_price, max_sell_price)) \
                 for quantity in [random.randint(0,max_sell_quentity) \
                                  for i in range(0,number_of_sell_trades,1)]])
    plot(pnl)
    pnl_ending.append(pnl[-1:][0])
    print 'step', step, 'pnl', pnl[-1:][0], 'avg. pnl', np.mean(pnl_ending), 'diff to mean', pnl[-1:][0]-np.mean(pnl_ending)
    
print 'avg, total pnl', np.mean(pnl_ending) #pnl[-1:][0]
show()

# bin the results
hist(pnl_ending, 25)
grid(True)
show()

# could lookat fitting and var.
