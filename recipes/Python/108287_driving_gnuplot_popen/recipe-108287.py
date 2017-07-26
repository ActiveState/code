import os
f=os.popen('gnuplot', 'w')
print >>f, "set yrange[-300:+300]"
for n in range(300):
	print >>f, "plot %i*cos(x)+%i*log(x+10)" % (n,150-n)
f.flush() 
