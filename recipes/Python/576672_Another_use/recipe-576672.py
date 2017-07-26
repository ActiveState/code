if bootstraps == 1:
  srri = lambda low, high, size: range(size) 
else:
  srri = scipy.random.random_integers

for boot in range(bootstraps):      
  for r in range(n1):
    for c in range(n0):
      sample_size = trial_result[r][c].size
      choices = srri(0, sample_size-1, sample_size)
      meas_grid[r,c] = pylab.array(trial_result[r][c][choices],dtype=float).mean()
  
  model_grid[:,:,:,boot], params[:,boot] = \
              process_grid(s0, s1, meas_grid)

#Instead of
srri = scipy.random.random_integers
if bootstraps == 1:
 for r in range(n1):
   for c in range(n0):
     meas_grid[r,c] = pylab.array(trial_result[r][c],dtype=float).mean()
  
 model_grid[:,:,:,boot], params[:,boot] = \
              process_grid(s0, s1, meas_grid)
else:
 for boot in range(bootstraps):
   for r in range(n1):
     for c in range(n0):
       sample_size = trial_result[r][c].size
       choices = srri(0, sample_size-1, sample_size)
       meas_grid[r,c] = pylab.array(trial_result[r][c][choices],dtype=float).mean()
  
   model_grid[:,:,:,boot], params[:,boot] = \
              process_grid(s0, s1, meas_grid)

#OR
srri = scipy.random.random_integers
for boot in range(bootstraps):
  if bootstraps == 1:
   for r in range(n1):
     for c in range(n0):
       meas_grid[r,c] = pylab.array(trial_result[r][c],dtype=float).mean()
  
    model_grid[:,:,:,boot], params[:,boot] = \
              process_grid(s0, s1, meas_grid)
  else:
   for r in range(n1):
     for c in range(n0):
       sample_size = trial_result[r][c].size
       choices = srri(0, sample_size-1, sample_size)
       meas_grid[r,c] = pylab.array(trial_result[r][c][choices],dtype=float).mean()
  
   model_grid[:,:,:,boot], params[:,boot] = \
              process_grid(s0, s1, meas_grid)
