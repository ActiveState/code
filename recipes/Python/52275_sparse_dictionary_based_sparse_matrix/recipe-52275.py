#!/usr/bin/env python

import vector
import math, types, operator

"""
A sparse matrix class based on a dictionary, supporting matrix (dot)
product and a conjugate gradient solver. 

In this version, the sparse class inherits from the dictionary; this
requires Python 2.2 or later.
"""

class sparse(dict):
	"""
	A complex sparse matrix 
	A. Pletzer 5 Jan 00/12 April 2002

	Dictionary storage format { (i,j): value, ... }
	where (i,j) are the matrix indices
       	"""

	# no c'tor

	def size(self):
		" returns # of rows and columns "
		nrow = 0
		ncol = 0
		for key in self.keys():
			nrow = max([nrow, key[0]+1])
			ncol = max([ncol, key[1]+1])
		return (nrow, ncol)

	def __add__(self, other):
		res = sparse(self.copy())
		for ij in other:
			res[ij] = self.get(ij,0.) + other[ij]
		return res
		
	def __neg__(self):
		return sparse(zip(self.keys(), map(operator.neg, self.values())))

	def __sub__(self, other):
		res = sparse(self.copy())
		for ij in other:
			res[ij] = self.get(ij,0.) - other[ij]
		return res
		
	def __mul__(self, other):
		" element by element multiplication: other can be scalar or sparse "
		try:
			# other is sparse
			nval = len(other)
			res = sparse()
			if nval < len(self):
				for ij in other:
					res[ij] = self.get(ij,0.)*other[ij]
			else:
				for ij in self:
					res[ij] = self[ij]*other.get(ij,0j)
			return res
		except:
			# other is scalar
			return sparse(zip(self.keys(), map(lambda x: x*other, self.values())))


	def __rmul__(self, other): return self.__mul__(other)

	def __div__(self, other):
		" element by element division self/other: other is scalar"
		return sparse(zip(self.keys(), map(lambda x: x/other, self.values())))
		
	def __rdiv__(self, other):
		" element by element division other/self: other is scalar"
		return sparse(zip(self.keys(), map(lambda x: other/x, self.values())))

	def abs(self):
		return sparse(zip(self.keys(), map(operator.abs, self.values())))

	def out(self):
		print '# (i, j) -- value'
		for k in self.keys():
			print k, self[k]

	def plot(self, width_in=400, height_in=400):

		import colormap
		import Tkinter

		cmax = max(self.values())
		cmin = min(self.values())
		
		offset =  0.05*min(width_in, height_in)
		xmin, ymin, xmax, ymax = 0,0,self.size()[0], self.size()[1]
		scale =  min(0.9*width_in, 0.9*height_in)/max(xmax-xmin, ymax-ymin)

		root = Tkinter.Tk()
		frame = Tkinter.Frame(root)
		frame.pack()
		
		text = Tkinter.Label(width=20, height=10, text='matrix sparsity')
		text.pack()
		

		canvas = Tkinter.Canvas(bg="black", width=width_in, height=height_in)
		canvas.pack()

		button = Tkinter.Button(frame, text="OK?", fg="red", command=frame.quit)
		button.pack()

		for index in self.keys():
			ix, iy = index[0], ymax-index[1]-1
			ya, xa = offset+scale*(ix  ), height_in -offset-scale*(iy  )
			yb, xb = offset+scale*(ix+1), height_in -offset-scale*(iy  )
			yc, xc = offset+scale*(ix+1), height_in -offset-scale*(iy+1)
			yd, xd = offset+scale*(ix  ), height_in -offset-scale*(iy+1)
			color = colormap.strRgb(self[index], cmin, cmax)
			canvas.create_polygon(xa, ya, xb, yb, xc, yc, xd, yd, fill=color)
		
		root.mainloop()

	def CGsolve(self, x0, b, tol=1.0e-10, nmax = 1000, verbose=1):
		"""
		Solve self*x = b and return x using the conjugate gradient method
		"""
		if not vector.isVector(b):
			raise TypeError, self.__class__,' in solve '
		else:
			if self.size()[0] != len(b) or self.size()[1] != len(b):
				print '**Incompatible sizes in solve'
				print '**size()=', self.size()[0], self.size()[1]
				print '**len=', len(b)
			else:
				kvec = diag(self) # preconditionner
				n = len(b)
				x = x0 # initial guess
				r =  b - dot(self, x)
				try:
					w = r/kvec
				except: print '***singular kvec'
				p = vector.zeros(n);
				beta = 0.0;
				rho = vector.dot(r, w);
				err = vector.norm(dot(self,x) - b);
				k = 0
				if verbose: print " conjugate gradient convergence (log error)"
				while abs(err) > tol and k < nmax:
					p = w + beta*p;
					z = dot(self, p);
					alpha = rho/vector.dot(p, z);
					r = r - alpha*z;
					w = r/kvec;
					rhoold = rho;
					rho = vector.dot(r, w);
					x = x + alpha*p;
					beta = rho/rhoold;
					err = vector.norm(dot(self, x) - b);
					if verbose: print k,' %5.1f ' % math.log10(err)
					k = k+1
				return x
				
		
	    		
	def biCGsolve(self,x0, b, tol=1.0e-10, nmax = 1000):
		
		"""
		Solve self*x = b and return x using the bi-conjugate gradient method
		"""

		try:
			if not vector.isVector(b):
				raise TypeError, self.__class__,' in solve '
			else:
				if self.size()[0] != len(b) or self.size()[1] != len(b):
					print '**Incompatible sizes in solve'
					print '**size()=', self.size()[0], self.size()[1]
					print '**len=', len(b)
				else:
					kvec = diag(self) # preconditionner 
					n = len(b)
					x = x0 # initial guess
					r =  b - dot(self, x)
					rbar =  r
					w = r/kvec;
					wbar = rbar/kvec;
					p = vector.zeros(n);
					pbar = vector.zeros(n);
					beta = 0.0;
					rho = vector.dot(rbar, w);
					err = vector.norm(dot(self,x) - b);
					k = 0
					print " bi-conjugate gradient convergence (log error)"
					while abs(err) > tol and k < nmax:
						p = w + beta*p;
						pbar = wbar + beta*pbar;
						z = dot(self, p);
						alpha = rho/vector.dot(pbar, z);
						r = r - alpha*z;
						rbar = rbar - alpha* dot(pbar, self);
						w = r/kvec;
						wbar = rbar/kvec;
						rhoold = rho;
						rho = vector.dot(rbar, w);
						x = x + alpha*p;
						beta = rho/rhoold;
						err = vector.norm(dot(self, x) - b);
						print k,' %5.1f ' % math.log10(err)
						k = k+1
					return x
			
		except: print 'ERROR ',self.__class__,'::biCGsolve'


	def save(self, filename, OneBased=0):
		"""
		Save matrix in file <filaname> using format:
		OneBased, nrow, ncol, nnonzeros
		[ii, jj, data]

		"""
		m = n = 0
		nnz = len(self)
		for ij in self.keys():
			m = max(ij[0], m)
			n = max(ij[1], n)

		f = open(filename,'w')
		f.write('%d %d %d %d\n' % (OneBased, m+1,n+1,nnz))
		for ij in self.keys():
			i,j = ij
			f.write('%d %d %20.17f \n'% \
				(i+OneBased,j+OneBased,self[ij]))
		f.close()
				
###############################################################################

def isSparse(x):
    return hasattr(x,'__class__') and x.__class__ is sparse

def transp(a):
	" transpose "
	new = sparse({})
	for ij in a:
		new[(ij[1], ij[0])] = a[ij]
	return new

def dotDot(y,a,x):
	" double dot product y^+ *A*x "
	if vector.isVector(y) and isSparse(a) and vector.isVector(x):
		res = 0.
		for ij in a.keys():
			i,j = ij
			res += y[i]*a[ij]*x[j]
		return res
	else:
		print 'sparse::Error: dotDot takes vector, sparse , vector as args'

def dot(a, b):
	" vector-matrix, matrix-vector or matrix-matrix product "
	if isSparse(a) and vector.isVector(b):
		new = vector.zeros(a.size()[0])
		for ij in a.keys():
			new[ij[0]] += a[ij]* b[ij[1]]
		return new
	elif vector.isVector(a) and isSparse(b):
		new = vector.zeros(b.size()[1])
		for ij in b.keys():
			new[ij[1]] += a[ij[0]]* b[ij]
		return new
	elif isSparse(a) and isSparse(b):
		if a.size()[1] != b.size()[0]:
			print '**Warning shapes do not match in dot(sparse, sparse)'
		new = sparse({})
		n = min([a.size()[1], b.size()[0]])
		for i in range(a.size()[0]):
			for j in range(b.size()[1]):
				sum = 0.
				for k in range(n):
					sum += a.get((i,k),0.)*b.get((k,j),0.)
				if sum != 0.:
					new[(i,j)] = sum
		return new
	else:
		raise TypeError, 'in dot'

def diag(b):
	# given a sparse matrix b return its diagonal
	res = vector.zeros(b.size()[0])
	for i in range(b.size()[0]):
		res[i] = b.get((i,i), 0.)
	return res
		
def identity(n):
	if type(n) != types.IntType:
		raise TypeError, ' in identity: # must be integer'
	else:
		new = sparse({})
		for i in range(n):
			new[(i,i)] = 1+0.
		return new

###############################################################################
if __name__ == "__main__":

	print 'a = sparse()'
	a = sparse()

	print 'a.__doc__=',a.__doc__

	print 'a[(0,0)] = 1.0'
	a[(0,0)] = 1.0
	a.out()

	print 'a[(2,3)] = 3.0'
	a[(2,3)] = 3.0
	a.out()

	print 'len(a)=',len(a)
	print 'a.size()=', a.size()
			
	b = sparse({(0,0):2.0, (0,1):1.0, (1,0):1.0, (1,1):2.0, (1,2):1.0, (2,1):1.0, (2,2):2.0})
	print 'a=', a
	print 'b=', b
	b.out()

	print 'a+b'
	c = a + b
	c.out()

	print '-a'
	c = -a
	c.out()
	a.out()

	print 'a-b'
	c = a - b
	c.out()

	print 'a*1.2'
	c = a*1.2
	c.out()


	print '1.2*a'
	c = 1.2*a
	c.out()
	print 'a=', a

	print 'dot(a, b)'
	print 'a.size()[1]=',a.size()[1],' b.size()[0]=', b.size()[0]
	c = dot(a, b)
	c.out()

	print 'dot(b, a)'
	print 'b.size()[1]=',b.size()[1],' a.size()[0]=', a.size()[0]
	c = dot(b, a)
	c.out()

	try:
		print 'dot(b, vector.vector([1,2,3]))'
		c = dot(b, vector.vector([1,2,3]))
		c.out()
	
		print 'dot(vector.vector([1,2,3]), b)'
		c = dot(vector.vector([1,2,3]), b)
		c.out()

		print 'b.size()=', b.size()
	except: pass
	
	print 'a*b -> element by element product'
	c = a*b
	c.out()

	print 'b*a -> element by element product'
	c = b*a
	c.out()
	
	print 'a/1.2'
	c = a/1.2
	c.out()

	print 'c = identity(4)'
	c = identity(4)
	c.out()

	print 'c = transp(a)'
	c = transp(a)
	c.out()


	b[(2,2)]=-10.0
	b[(2,0)]=+10.0

	try:
		import vector
		print 'Check conjugate gradient solver'
		s = vector.vector([1, 0, 0])
		print 's'
		s.out()
		x0 = s 
		print 'x = b.biCGsolve(x0, s, 1.0e-10, len(b)+1)'
		x = b.biCGsolve(x0, s, 1.0e-10,  len(b)+1)
		x.out()

		print 'check validity of CG'
		c = dot(b, x) - s
		c.out()
	except: pass

	print 'plot b matrix'
	b.out()
	b.plot()

	print 'del b[(2,2)]'
	del b[(2,2)]

	print 'del a'
	del a
	#a.out()
