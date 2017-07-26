f=lambda ss,row=[],level=0: len(ss)>1 \
   and reduce(lambda x,y:x+y,[f(ss[1:],row+[i],level+1) for i in ss[0]]) \
   or [row+[i] for i in ss[0]]

# Example:

# If you have some sets ...

s1=['a1','a2','a3','a4']
s2=['b1','b2']
s3=['c1','c2','c3']

# ... simply put them in a "super=set" ...
ss=[s1,s2,s3]

# ... and call the function
cross_product =f(ss)

# this is the result
assert cross_product==[['a1', 'b1', 'c1'],
                      ['a1', 'b1', 'c2'],
                      ['a1', 'b1', 'c3'],
                      ['a1', 'b2', 'c1'],
                      ['a1', 'b2', 'c2'],
                      ['a1', 'b2', 'c3'],
                      ['a2', 'b1', 'c1'],
                      ['a2', 'b1', 'c2'],
                      ['a2', 'b1', 'c3'],
                      ['a2', 'b2', 'c1'],
                      ['a2', 'b2', 'c2'],
                      ['a2', 'b2', 'c3'],
                      ['a3', 'b1', 'c1'],
                      ['a3', 'b1', 'c2'],
                      ['a3', 'b1', 'c3'],
                      ['a3', 'b2', 'c1'],
                      ['a3', 'b2', 'c2'],
                      ['a3', 'b2', 'c3'],
                      ['a4', 'b1', 'c1'],
                      ['a4', 'b1', 'c2'],
                      ['a4', 'b1', 'c3'],
                      ['a4', 'b2', 'c1'],
                      ['a4', 'b2', 'c2'],
                      ['a4', 'b2', 'c3']],\
                      'cros sproduct failed'
