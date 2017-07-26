X = m.matrix(numpy.random.standard_normal((3,1000)))  
C = m.matrix(m.array([[1,.3,.3],[.3,1.,.3],[.3,.3,1.]]))
U = m.cholesky(C)
Y = U*X

#And to test that this works:

m.corrcoef(Y[0,:],Y[1,:])
m.corrcoef(Y[0,:],Y[2,:])
m.corrcoef(Y[1,:],Y[2,:])
