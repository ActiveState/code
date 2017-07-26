# agents
# agent_id, agent_famname,agent_name
t1=[[100,'Brown','Jack'],
    [101,'Red','James'],
    [102,'Black','John'],
    [103,'White','Jeff'],
    [104,'White','Jasper']]

# clients
# client_id,agent_id,client_name
t2=[[100,100,'McDonalds'],
    [101,100,'KFC'],
    [102,102,'Burger King'],
    [103,103,'Chinese'],
    [104,999,'French']]

# more agents /agents1
# agent_id, agent_famname,agent_name
t3=[[200,'Smith','Jack'],
    [101,'Red','James'],
    [201,'Carpenter','John'],
    [103,'White','Jeff']]



# restriction
# SQL: select * from agents where agent_famname='White'

res=[row for row in t1 if row[1]=='White']

assert res == [[103, 'White', 'Jeff'],
               [104, 'White', 'Jasper']], \
               'restriction failed'


# projection
# SQL: select agent_name,agent_famname from agents

res=[[row[2],row[1]] for row in t1 ]

assert res == [['Jack', 'Brown'],
               ['James', 'Red'],
               ['John', 'Black'],
               ['Jeff', 'White'],
               ['Jasper', 'White']],\
               'projection failed'
               

# cross-product (cartesian product)
# SQL: select * from agents, clients

res= [r1+r2 for r1 in t1 for r2 in t2 ]

assert res == [[100, 'Brown', 'Jack', 100, 100, 'McDonalds'],
               [100, 'Brown', 'Jack', 101, 100, 'KFC'],
               [100, 'Brown', 'Jack', 102, 102, 'Burger King'],
               [100, 'Brown', 'Jack', 103, 103, 'Chinese'],
               [100, 'Brown', 'Jack', 104, 999, 'French'],
               [101, 'Red', 'James', 100, 100, 'McDonalds'],
               [101, 'Red', 'James', 101, 100, 'KFC'],
               [101, 'Red', 'James', 102, 102, 'Burger King'],
               [101, 'Red', 'James', 103, 103, 'Chinese'],
               [101, 'Red', 'James', 104, 999, 'French'],
               [102, 'Black', 'John', 100, 100, 'McDonalds'],
               [102, 'Black', 'John', 101, 100, 'KFC'],
               [102, 'Black', 'John', 102, 102, 'Burger King'],
               [102, 'Black', 'John', 103, 103, 'Chinese'],
               [102, 'Black', 'John', 104, 999, 'French'],
               [103, 'White', 'Jeff', 100, 100, 'McDonalds'],
               [103, 'White', 'Jeff', 101, 100, 'KFC'],
               [103, 'White', 'Jeff', 102, 102, 'Burger King'],
               [103, 'White', 'Jeff', 103, 103, 'Chinese'],
               [103, 'White', 'Jeff', 104, 999, 'French'],
               [104, 'White', 'Jasper', 100, 100, 'McDonalds'],
               [104, 'White', 'Jasper', 101, 100, 'KFC'],
               [104, 'White', 'Jasper', 102, 102, 'Burger King'],
               [104, 'White', 'Jasper', 103, 103, 'Chinese'],
               [104, 'White', 'Jasper', 104, 999, 'French']],\
               'cross product failed'
               
# equi join / inner join
# SQL: select agents.*, clients.* from agents,clients
#      where agents.agent_id=clients.agent_id

res= [r1+r2 for r1 in t1 for r2 in t2 if r1[0]==r2[1]]

assert res == [[100, 'Brown', 'Jack', 100, 100, 'McDonalds'],
               [100, 'Brown', 'Jack', 101, 100, 'KFC'],
               [102, 'Black', 'John', 102, 102, 'Burger King'],
               [103, 'White', 'Jeff', 103, 103, 'Chinese']],\
               'inner join failed'

               
# left outer join
# SQL: select agents.*, clients.* from agents left outer join clients
#      where agents.agent_id = clients.agent_id

res= [r1+r2 for r1 in t1 for r2 in t2 if r1[0]==r2[1]]+\
     [r1+[None]*len(t2[0]) for r1 in t1 if r1[0] not in [r2[1] for r2 in t2]]

assert res == [[100, 'Brown', 'Jack', 100, 100, 'McDonalds'],
               [100, 'Brown', 'Jack', 101, 100, 'KFC'],
               [102, 'Black', 'John', 102, 102, 'Burger King'],
               [103, 'White', 'Jeff', 103, 103, 'Chinese'],
               [101, 'Red', 'James', None, None, None],
               [104, 'White', 'Jasper', None, None, None]],\
               'left outer join failed'

               
# right outer join
# SQL: select agents.*, clients.* from agents right outer join clients
#      where agents.agent_id = clients.agent_id

res= [r1+r2 for r1 in t1 for r2 in t2 if r1[0]==r2[1]]+\
     [[None]*len(t1[0])+r2 for r2 in t2 if r2[1] not in [r1[0] for r1 in t1]]

assert res == [[100, 'Brown', 'Jack', 100, 100, 'McDonalds'],
               [100, 'Brown', 'Jack', 101, 100, 'KFC'],
               [102, 'Black', 'John', 102, 102, 'Burger King'],
               [103, 'White', 'Jeff', 103, 103, 'Chinese'],
               [None, None, None, 104, 999, 'French']],\
               'right outer join failed'


# full outer join
# SQL: select agents.*, clients.* from agents full outer join clients
#      where agents.agent_id = clients.agent_id

res= [r1+r2 for r1 in t1 for r2 in t2 if r1[0]==r2[1]]+\
     [r1+[None]*len(t2[0]) for r1 in t1 if r1[0] not in [r2[1] for r2 in t2]]+\
     [[None]*len(t1[0])+r2 for r2 in t2 if r2[1] not in [r1[0] for r1 in t1]]

assert res == [[100, 'Brown', 'Jack', 100, 100, 'McDonalds'],
               [100, 'Brown', 'Jack', 101, 100, 'KFC'],
               [102, 'Black', 'John', 102, 102, 'Burger King'],
               [103, 'White', 'Jeff', 103, 103, 'Chinese'],
               [101, 'Red', 'James', None, None, None],
               [104, 'White', 'Jasper', None, None, None],
               [None, None, None, 104, 999, 'French']],\
               'full join failed'
               

# union
# SQL: select * from agents union select * from agents1

res=t1+[r2 for r2 in t3 if r2 not in t1]

assert res == [[100, 'Brown', 'Jack'],
               [101, 'Red', 'James'],
               [102, 'Black', 'John'],
               [103, 'White', 'Jeff'],
               [104, 'White', 'Jasper'],
               [200, 'Smith', 'Jack'],
               [201, 'Carpenter', 'John']], \
               'union failed'


# intersection
# SQL: select * from agents intersect select * from agents1

res=[r2 for r2 in t3 if r2 in t1]

assert res == [[101, 'Red', 'James'],
               [103, 'White', 'Jeff']], \
               'intersection failed'


# difference
# SQL: select * from agents minus select * from agents1

res=[r1 for r1 in t1 if r1 not in t3]

assert res == [[100, 'Brown', 'Jack'],
               [102, 'Black', 'John'],
               [104, 'White', 'Jasper']], \
               'difference failed'
