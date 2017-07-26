#get nth fibonacci number for n < = 0 returns 1
fib = lambda n,a=1,b=1:n-1 + abs(n-1) and fib(n-1,b,a+b) or b
#another version
fib = lambda n,a=1,b=1:[b,0][n>0] or fib(n-1,b,a+b)
