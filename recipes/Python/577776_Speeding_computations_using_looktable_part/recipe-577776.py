import pylab
import scipy.stats as ss
nrm = ss.norm
nx = nrm.pdf

# Lookup table based implementations ------------------------------------------
def init_nx_table(xlim=5,N=1001):
  """Go from -xlim to +xlim and make N entries, return us the dx and x0.
  if N is made odd it is better"""
  idx0 = int(N/2)
  tbl = pylab.zeros(N)  
  x = pylab.linspace(-xlim,xlim,N)
  dx = x[1] - x[0]
  tbl = nx(x)
  return x, tbl, idx0, dx

def nx_lookup(x,mu,tbl, idx0, dx):
  """x needs to be an array."""
  sz = tbl.size
  ret = pylab.zeros(x.size) #Our results
  idx = (x-mu)/dx + idx0  + .5 #indexes into our table need +.5 because of rounding
  idxidx = pylab.find((idx>=0) & (idx<sz)) #indexes of valid indexes
  ret[idxidx] = tbl[idx[idxidx].astype('int16')]
  return ret

def testnx(dotiming=False):
  xtbl, tbl, idx0, dx = init_nx_table()
  
  if dotiming:
    import cProfile
    x = pylab.linspace(-10,10,1000000)
    cProfile.runctx('nx(x)',globals(),locals())
    cProfile.runctx('nx_lookup(x, 0, tbl, idx0, dx)',globals(),locals())
    cProfile.runctx('pylab.interp(x, xtbl, tbl, left=0, right=0)',globals(),locals())
  else:
    x = pylab.linspace(-10,10,1000)
    x0 = nx(x)
    x1 = nx_lookup(x, 0, tbl, idx0, dx)
    x2 = pylab.interp(x, xtbl, tbl, left=0, right=0)
    pylab.plot(x, x0-x1)
    pylab.plot(x, x0-x2)
    pylab.ylabel('Error')

if __name__ == "__main__":
  testnx()
  testnx(True)
