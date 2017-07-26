nl= (2,3,6,18)

# The sum comprehension
[ [ [j for j in (j+i,) ] for i in nl] for j in (0,) ]  [0][-1][0]
# results in 29 or [[[2], [5], [11], [29]]]  without   [0][-1][0] at the tail

# the product comprehension
[ [ [j for j in (j*i,)] for i in nl ] for j in (1,) ]  [0][-1][0]
# results in 648 when nl = (2,3,6,18)

# a factorial comprehension
fac= 6
[ [ [j for j in (j*i,)] for i in range(2,fac+1)] for j in (1,)]   [0][-1][0]
# results in 720
