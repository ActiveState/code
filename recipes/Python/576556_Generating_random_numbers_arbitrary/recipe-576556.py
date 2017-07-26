import pylab
import numpy

class GeneralRandom:
  """This class enables us to generate random numbers with an arbitrary 
  distribution."""
  
  def __init__(self, x = pylab.arange(-1.0, 1.0, .01), p = None, Nrl = 1000):
    """Initialize the lookup table (with default values if necessary)
    Inputs:
    x = random number values
    p = probability density profile at that point
    Nrl = number of reverse look up values between 0 and 1"""  
    if p == None:
      p = pylab.exp(-10*x**2.0)
    self.set_pdf(x, p, Nrl)
    
  def set_pdf(self, x, p, Nrl = 1000):
    """Generate the lookup tables. 
    x is the value of the random variate
    pdf is its probability density
    cdf is the cumulative pdf
    inversecdf is the inverse look up table
    
    """
    
    self.x = x
    self.pdf = p/p.sum() #normalize it
    self.cdf = self.pdf.cumsum()
    self.inversecdfbins = Nrl
    self.Nrl = Nrl
    y = pylab.arange(Nrl)/float(Nrl)
    delta = 1.0/Nrl
    self.inversecdf = pylab.zeros(Nrl)    
    self.inversecdf[0] = self.x[0]
    cdf_idx = 0
    for n in xrange(1,self.inversecdfbins):
      while self.cdf[cdf_idx] < y[n] and cdf_idx < Nrl:
        cdf_idx += 1
      self.inversecdf[n] = self.x[cdf_idx-1] + (self.x[cdf_idx] - self.x[cdf_idx-1]) * (y[n] - self.cdf[cdf_idx-1])/(self.cdf[cdf_idx] - self.cdf[cdf_idx-1]) 
      if cdf_idx >= Nrl:
        break
    self.delta_inversecdf = pylab.concatenate((pylab.diff(self.inversecdf), [0]))
              
  def random(self, N = 1000):
    """Give us N random numbers with the requested distribution"""

    idx_f = numpy.random.uniform(size = N, high = self.Nrl-1)
    idx = pylab.array([idx_f],'i')
    y = self.inversecdf[idx] + (idx_f - idx)*self.delta_inversecdf[idx]

    return y
  
  def plot_pdf(self):
    pylab.plot(self.x, self.pdf)
    
  def self_test(self, N = 1000):
    pylab.figure()
    #The cdf
    pylab.subplot(2,2,1)
    pylab.plot(self.x, self.cdf)
    #The inverse cdf
    pylab.subplot(2,2,2)
    y = pylab.arange(self.Nrl)/float(self.Nrl)
    pylab.plot(y, self.inversecdf)
    
    #The actual generated numbers
    pylab.subplot(2,2,3)
    y = self.random(N)
    p1, edges = pylab.histogram(y, bins = 50, 
                                range = (self.x.min(), self.x.max()), 
                                normed = True, new = True)
    x1 = 0.5*(edges[0:-1] + edges[1:])
    pylab.plot(x1, p1/p1.max())
    pylab.plot(self.x, self.pdf/self.pdf.max())
