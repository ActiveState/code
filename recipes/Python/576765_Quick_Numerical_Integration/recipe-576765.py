# simple integration

from scipy import integrate

f_x = [1, 1.22, 1.41, 1.58, 1.73]

x_n = 1.0
x_0 = 0.0

h = (x_n-x_0)/(len(f_x)-1)
print 'h ['+str(h)+']'
print 'trapz ['+str(integrate.trapz(f_x, dx=h)) + ']'
print 'cumtrapz ['+str(integrate.cumtrapz(f_x, dx=h)) + ']'
print 'simpson ['+str(integrate.simps(f_x, dx=h)) + ']'

#print integrate.trapz([1,1.22,1.41,1.58,1.73], [0,0.25,0.5, 0.75, 1])
#print integrate.trapz([1,1.22,1.41,1.58,1.73], dx=0.25)
#print integrate.cumtrapz([1,1.22,1.41,1.58,1.73], dx=0.25)
#print integrate.simps([1,1.22,1.41,1.58,1.73], [0,0.25,0.5, 0.75, 1])
