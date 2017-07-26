from numpy import array, mat, shape, transpose
from scipy import cov, linalg
from pylab import load, arange

data2 = mat(array(load('raw3.dat', delimiter='\t',usecols=arange(0,13,1), unpack=True)))
time_series = mat(cov(data2, rowvar=1))
print 'covariance matrix : ', shape(time_series)
eval, evec = linalg.eig(mat(time_series))
print shape(eval), shape(evec)
print abs(evec)
print abs(eval)
