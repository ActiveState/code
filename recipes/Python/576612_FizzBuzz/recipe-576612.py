n=map(str, range(101))
n[::3]=['Fizz']*34
n[::5]=['Buzz']*21
n[::15]=['FizzBuzz']*7
print '\n'.join(n[1:])
