"""Polynomial explorer. You tell this module what order of polynomial you want and it will set up a figure
with a graph of that polynomial plotted with x = -1 to +1. It will set up a second figure with a set of
coefficient axes. You can click on the coeffiecient axes to set the coefficents. The graph will then update 
to reflect the values of the new coefficients"""

import pylab as M

def f(x,c):
	"""Pass in x (a scalar or vector) and pass in c (a vector) and this function will compute 
f(x) = x**n + c(n-1)*x**(n-1) ... + c(1)*x + c(0)"""
	
	N = len(c)
	y = M.zeros(len(x))
	for n in xrange(N):
		y += c[n]*x**n
	y += x**N
		
	return y

def fstring(c):
	"""Pass the coefficients and return a string corresponding to the ploynomial"""
	
	order = len(c)
	fx = "$f(x) = x^%d" %(order)
	for n in xrange(order-1):
		nn = order - 1 - n 
		fx += " + %1.3f x^%d" %(c[nn],nn)
	fx += " + %1.3f$" %(c[0])
	
	return fx


class Explorer:
	
	def __init__(self, norder = 2):
		"""Initializes the class when returning an instance. Pass it the polynomial order. It will 
set up two figure windows, one for the graph the other for the coefficent interface. It will then initialize 
the coefficients to zero and plot the (not so interesting) polynomial."""
		
		self.order = norder
		
		self.c = M.zeros(self.order,'f')
		self.ax = [None]*(self.order-1)#M.zeros(self.order-1,'i') #Coefficent axes
		
		self.ffig = M.figure() #The first figure window has the plot
		self.replotf()
		
		self.cfig = M.figure() #The second figure window has the 
		row = M.ceil(M.sqrt(self.order-1))
		for n in xrange(self.order-1):
			self.ax[n] = M.subplot(row, row, n+1)
			M.setp(self.ax[n],'label', n)
			M.plot([0],[0],'.')
			M.axis([-1, 1, -1, 1]);
			
		self.replotc()
		M.connect('button_press_event', self.click_event)
	
	def replotf(self):
		"""This replots the function given the coefficient array c."""

		x = M.arange(-1,1.,.001)
		M.ioff()
		M.figure(self.ffig.number)
		M.cla()
		M.plot(x, f(x,self.c))				
		M.title(fstring(self.c))
		M.draw()
		
	def replotc(self):
		"""This replots the coefficients."""
	
		M.figure(self.cfig.number)
		M.ioff()
		for n in xrange(self.order-1):
			M.axes(self.ax[n])
			#M.cla()
			M.plot([self.c[n]], [self.c[n+1]],'ko')
			M.xlabel("$c_%d$" %(n))
			M.ylabel("$c_%d$" %(n+1))
			M.axis([-1, 1, -1, 1]);
			del self.ax[n].lines[0]

		M.draw()
		
	def click_event(self, event):
		"""Whenever a click occurs on the coefficent axes we modify the coefficents and update the 
plot"""
		
		if event.xdata is None:#we clicked outside the axis
			return

		idx = M.getp(event.inaxes,'label')
		
		print idx, event.xdata, event.ydata
				
		self.c[idx] = event.xdata
		self.c[idx+1] = event.ydata

		self.replotf()
		self.replotc()
