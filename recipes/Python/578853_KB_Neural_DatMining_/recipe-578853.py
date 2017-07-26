# -*- coding: utf-8 -*-
############################################################################### 
# KB_CAT KNOWLEDGE DISCOVERY IN DATA MINING (CATALOG PROGRAM)                 # 
# by ROBERTO BELLO (COPYRIGHT MARCH 2011 ALL RIGHTS RESERVED)                 # 
# Language used: PYTHON                               .                       # 
############################################################################### 
import os
import random
import copy
import datetime

def mean(x):     	# mean
  n = len(x)
  mean = sum(x) / n
  return mean

def sd(x):		# standard deviattion
  n = len(x)
  mean = sum(x) / n
  sd = (sum((x-mean)**2 for x in x) / n) ** 0.5
  return sd

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

class ndim:             # from 3D array to flat array
    def __init__(self,x,y,z,d):
        self.dimensions=[x,y,z]
        self.numdimensions=d
        self.gridsize=x*y*z

    def getcellindex(self, location):
        cindex = 0
        cdrop = self.gridsize
        for index in xrange(self.numdimensions):
            cdrop /= self.dimensions[index]
            cindex += cdrop * location[index]
        return cindex

    def getlocation(self, cellindex):
        res = []
        for size in reversed(self.dimensions):
            res.append(cellindex % size)
            cellindex /= size
        return res[::-1]

""" how to use ndim class
n=ndim(4,4,5,3)
print n.getcellindex((0,0,0))
print n.getcellindex((0,0,1))
print n.getcellindex((0,1,0))
print n.getcellindex((1,0,0))

print n.getlocation(20)
print n.getlocation(5)
print n.getlocation(1)
print n.getlocation(0)
"""

print("###############################################################################")
print("# KB_CAT KNOWLEDGE DISCOVERY IN DATA MINING (CATALOG PROGRAM)                 #")
print("# by ROBERTO BELLO (COPYRIGHT MARCH 2011 ALL RIGHTS RESERVED)                 #")
print("# Language used: PYTHON                                                       #")
print("###############################################################################") 

# input and run parameters
error = 0

while True:
  arch_input = raw_input('InputFile                              : ')
  if not os.path.isfile(arch_input):
    print("Oops! File does not exist. Try again... or CTR/C to exit")     
  else:
    break

while True:
  try:
    num_gruppi = int(raw_input('Number of Groups (3 - 20)              : '))
  except ValueError:
    print("Oops!  That was no valid number.  Try again...")
  else:
    if(num_gruppi < 3):
      print("Oops! Number of Groups too low. Try again...")
    else:
      if(num_gruppi > 20):
        print("Oops! Number of Groups too big. Try again...")
      else:
        break

while True:
  normaliz   = raw_input('Normalization(Max, Std, None)          : ')
  normaliz   = normaliz.upper()
  normaliz   = normaliz[0]
  if(normaliz <> 'M' and normaliz <> 'S' and normaliz <> 'N'):
    print("Oops! Input M, S or N. Try again...")
  else:
    break

while True:
  try:
    max_alpha   = float(raw_input('Start value of alpha (1.8 - 0.9)       : '))
  except ValueError:
    print("Oops!  That was no valid number.  Try again...")
  else:
    if(max_alpha > 1.8):
      print("Oops! Start value of alpha too big. Try again...")
    else:
      if(max_alpha < 0.9):
        print("Oops! Start value of alpha too low. Try again...")
      else:
        break

while True:
  try:
    min_alpha  = float(raw_input('End value of alpha (0.5 - 0.0001)      : '))
  except ValueError:
    print("Oops!  That was no valid number.  Try again...")
  else:
    if(min_alpha > 0.5):
      print("Oops! alpha too big. Try again...")
    else:
      if(min_alpha < 0.0001):
        print("Oops! alpha too low. Try again...")
      else:
        break

while True:
  try:
    step_alpha  = float(raw_input('Decreasing step of alpha (0.1 - 0.001) : '))
  except ValueError:
    print("Oops!  That was no valid number.  Try again...")
  else:
    if(step_alpha > 0.1):
      print("Oops! Decreasing step of alpha too big. Try again...")
    else:
      if(step_alpha < 0.001):
        print("Oops! Decreasing step of alpha too low. Try again...")
      else:
        break


file_input   = arch_input 
gruppi_num   = num_gruppi
tipo_norm    = normaliz 
alpha_min    = min_alpha 
alpha_max    = max_alpha
alpha_step   = step_alpha

# outputs files
file_input   = arch_input
tipo_norm    = normaliz
gruppi_num   = num_gruppi
nome_input   = file_input.split(".") 
arch_output  = nome_input[0] + "_" + tipo_norm + "_g" + str(gruppi_num) + "_out.txt" 
arch_outsrt  = nome_input[0] + "_" + tipo_norm + "_g" + str(gruppi_num) + "_outsrt.txt" 
arch_sort    = nome_input[0] + "_" + tipo_norm + "_g" + str(gruppi_num) + "_sort.txt" 
arch_catal   = nome_input[0] + "_" + tipo_norm + "_g" + str(gruppi_num) + "_catal.txt" 
arch_medsd   = nome_input[0] + "_" + tipo_norm + "_g" + str(gruppi_num) + "_medsd.txt" 
arch_cv      = nome_input[0] + "_" + tipo_norm + "_g" + str(gruppi_num) + "_cv.txt" 
arch_grid    = nome_input[0] + "_" + tipo_norm + "_g" + str(gruppi_num) + "_grid.txt" 
arch_log     = nome_input[0] + "_" + tipo_norm + "_g" + str(gruppi_num) + "_log.txt" 

# start time
t0 = datetime.datetime.now()

# read input file 
arr_r    = [] 
arr_orig = [] 
arr_c    = [] 
mtchx    = [] 
mtchy    = [] 
txt_col  = [] 
xnomi    = [] 

# the numbers of variables / columns in all record must be the same 
n_rows = 0 
n_cols = 0 
err_cols = 0 
index = 0 
for line in open(file_input).readlines():
  linea = line.split()
  if(index == 0):
    xnomi.append(linea)
    n_cols = len(linea)
  else:
    arr_r.append(linea)
    if(len(linea) != n_cols):
      err_cols = 1
      print("Different numbers of variables / columns in the record " + str(index)
        + " cols " + str(len(linea))) 
  index += 1
if(err_cols == 1):
  print("File " + file_input + " contains errors. Exit ")
  quit()
index = 0
while index < len(arr_r):
  linea = arr_r[index]
  index_c = 0
  while index_c < len(linea):
    if linea[index_c].isdigit():
      linea[index_c] = float(linea[index_c])
    index_c += 1
  arr_r[index] = linea 
  index += 1
arr_orig = copy.deepcopy(arr_r)        # original input file
testata_cat = copy.deepcopy(xnomi[0])  # original header row

# finding columns containing strings and columns containing numbers
testata = xnomi[0]
testata_orig = copy.deepcopy(xnomi[0])
n_cols = len(testata) - 1
n_rows = len(arr_r)
ind_c  = 1
err_type = 0
while ind_c < len(testata):
  ind_r    = 1
  tipo_num = 0 
  tipo_txt = 0 
  while ind_r < len(arr_r):

    arr_c = arr_r[ind_r]

    if is_number(arr_c[ind_c]):
      tipo_num = 1
    else:
      tipo_txt = 1

    ind_r += 1

  if tipo_num == 1 and tipo_txt == 1:
    print "The columns / variables " + testata[ind_c] + " contains both strings and numbers." 
    print arr_c
    err_type = 1 
  ind_c += 1
if err_type == 1:
  print "Oops! The columns / variables contains both strings and numbers. Exit. " 
  quit()

index_c = 1 
while index_c <= n_cols:
  txt_col = [] 
  index = 0 
  while index < len(arr_r):
    arr_c = arr_r[index] 
    if(isinstance(arr_c[index_c],str)):
      txt_col.append(arr_c[index_c]) 
    index += 1 
  set_txt_col = set(txt_col)             # remove duplicates 
  txt_col = list(set(set_txt_col))
  txt_col.sort()
  
  # from strings to numbers 
  if(len(txt_col) > 0): 
    if(len(txt_col) > 1): 
      passo1 = 1.0 / (len(txt_col) - 1) 
    else:
      passo1 = 0.0
    index = 0
    while index < len(arr_r): 
      arr_c = arr_r[index] 
      campo1 = arr_c[index_c] 
      indice1 = txt_col.index(campo1) 
      if(len(txt_col) == 1):  # same values in the column
        val_num1 = float(1) 
      else: 
        val_num1 = float(passo1 * indice1)
      arr_c[index_c] = val_num1 + 0.00000001   # to avoid zero values in means
                                               # (to prevent zero divide in CV)
      index += 1 
  index_c += 1 

# means, max & std 
xmeans = [] 
xmaxs  = [] 
xmins  = []            ### aggiunto Roberto 4/03/2012
xsds   = [] 
xcv    = [] 
index_c = 0
while index_c <= n_cols:
  xmeans.append(0.0) 
  xmaxs.append(-9999999999999999.9) 
  xmins.append(9999999999999999.9)	### aggiunto Roberto 4/03/2012
  xsds.append(0.0) 
  xcv.append(0.0)
  index_c += 1 

# means & max
index = 0 
while index < n_rows:
  arr_c = arr_r[index] 
  index_c = 1 
  while index_c <= n_cols:
    xmeans[index_c] += arr_c[index_c] 
    if(arr_c[index_c] > xmaxs[index_c]):
      xmaxs[index_c] = arr_c[index_c] 
    index_c += 1 
  index += 1 
index_c = 1 
while index_c <= n_cols:
  xmeans[index_c] = xmeans[index_c] / n_rows
  index_c += 1 

# std
index = 0 
while index < n_rows:
  arr_c = arr_r[index] 
  index_c = 1 
  while index_c <= n_cols:
    xsds[index_c] += (arr_c[index_c] - xmeans[index_c])**2 
    index_c += 1 
  index += 1 
index_c = 1 

while index_c <= n_cols:
  xsds[index_c] = (xsds[index_c] / (n_cols - 1)) ** 0.5 
  index_c += 1 

# Means, Max, Std, CV output file
medsd_file = open(arch_medsd, 'w')
  
# columns names
medsd_file.write('%s %s ' % ('Function' , "\t"))
index_c = 1 
while index_c <= n_cols:
  medsd_file.write('%s %s ' % (testata[index_c], "\t"))
  index_c += 1
medsd_file.write('%s' % ('\n'))

# means
medsd_file.write('%s %s ' % ('Mean' , "\t"))
index_c = 1 
while index_c <= n_cols:
  valore = str(xmeans[index_c]) 
  valore = valore[0:6] 
  medsd_file.write('%s %s ' % (valore, "\t")) 
  index_c += 1 
medsd_file.write('%s' % ('\n'))

# max
medsd_file.write('%s %s ' % ('Max' , "\t"))
index_c = 1 
while index_c <= n_cols:
  valore = str(xmaxs[index_c]) 
  valore = valore[0:6] 
  medsd_file.write('%s %s ' % (valore, "\t")) 
  index_c += 1 
medsd_file.write('%s' % ('\n'))

# std
medsd_file.write('%s %s ' % ('Std' , "\t"))
index_c = 1 
while index_c <= n_cols:
  valore = str(xsds[index_c]) 
  valore = valore[0:6] 
  medsd_file.write('%s %s ' % (valore, "\t")) 
  index_c += 1 
medsd_file.write('%s' % ('\n'))

# CV 
medsd_file.write('%s %s ' % ('CV' , "\t"))
index_c = 1 
med_cv_gen = 0.0 		# cv average of all columns / variables
while index_c <= n_cols:
  if xmeans[index_c] == 0: 
    media1 = 0.000001 
  else:
    media1 = xmeans[index_c] 
  xcv[index_c] = xsds[index_c] / abs(media1) 
  valore = str(xcv[index_c])
  med_cv_gen += xcv[index_c]
  valore = valore[0:6] 
  medsd_file.write('%s %s ' % (valore, "\t")) 
  index_c += 1 
med_cv_gen = med_cv_gen / n_cols
str_med_cv_gen = str(med_cv_gen)
str_med_cv_gen = str_med_cv_gen[0:6]
medsd_file.write('%s' % ('\n'))
medsd_file.close()

# input standardization

# standardization on max

if tipo_norm == 'M':
  index = 0
  while index < n_rows:
    arr_c = arr_r[index] 
    index_c = 1 
    while index_c <= n_cols:    ## aggiornare anche kb_cla.py
      if xmaxs[index_c] == 0.0:
        xmaxs[index_c] = 0.00001 
      arr_c[index_c] = arr_c[index_c] / xmaxs[index_c] 
      index_c += 1 
    index += 1 

# standardization on std

if tipo_norm == 'S':
  index = 0
  while index < n_rows: 
    arr_c = arr_r[index] 
    index_c = 1 
    while index_c <= n_cols:    
      if xsds[index_c] == 0.0:
        xsds[index_c] = 0.00001 
      arr_c[index_c] = (arr_c[index_c] - xmeans[index_c]) / xsds[index_c]
      if arr_c[index_c] < xmins[index_c]:	### aggiunto Roberto 4/03/2012
        xmins[index_c] = arr_c[index_c]       	### aggiunto Roberto 4/03/2012
      index_c += 1 
    index += 1 
  # aggiungo xmins per eliminare i valori negativi (aggiunto da Roberto 4/03/2012)
  index = 0
  while index < n_rows: 
    arr_c = arr_r[index] 
    index_c = 1 
    while index_c <= n_cols:    
      arr_c[index_c] = arr_c[index_c] - xmins[index_c]
      print arr_c[index_c]
      index_c += 1 
    index += 1 
  # fine aggiunta da Roberto 4/03/2012

# start of kohonen algorithm 

# min and max vectors

vmaxs = []
vmins = []

index_c = 0

while index_c <= n_cols:
  vmaxs.append(-10000000000000.0) 
  vmins.append( 10000000000000.0) 
  index_c += 1 

# columns min & max 
index = 0
while index < n_rows:
  arr_c = arr_r[index] 
  index_c = 1 
  while index_c <= n_cols:
    if arr_c[index_c] > vmaxs[index_c]:
      vmaxs[index_c] = arr_c[index_c] 
    if arr_c[index_c] < vmins[index_c]:
      vmins[index_c] = arr_c[index_c] 
    index_c += 1 
  index += 1 

# run parameters and temp arrays
  
n = n_rows
m = n_cols
nx = gruppi_num 
ny = gruppi_num 
ix = 950041                         # integer as random seed
nsteps = int(10000 * nx * ny)       # number of steps
nepoks = int(nsteps / n ** 0.5)     # number of epochs
unit_calc = int(n * m * nx * ny)    # running units
passo = int(5000 / n)               # step of visualization on monitor
rmax = nx - 1
rmin = 1.0 

if passo < 1:
  passo = 1 
grid = []			    # training grid
index = 0
while index < nx * ny * m:
  grid.append(0.0)
  index += 1
n=ndim(nx,ny,m,3)
random.seed(ix)	       		    # initial value of random seed to obtain the same sequences in new runs
index = 0 
while index < nx: 
  index_c = 0 
  while index_c < ny:
    index_k = 0 
    while index_k < m: 
      ig = n.getcellindex((index,index_c,index_k))
      grid[ig] = random.random()
      index_k += 1 
    index_c += 1 
  index += 1 
gridp = copy.deepcopy(grid)     # initial previous grid = current grid 
gridm = copy.deepcopy(grid)     # initial min grid = current grid 

# for each record in each epoch 
iter 	  = 0 
discrea   = 1000000000000.0 	# current error
discrep   = 0.0 		# previous error
if nepoks < 20: 
  nepoks  = 20 			# min epochs = 20
nepokx    = 0
min_epok  = 0          		# epoch with min error
min_err   = 1000000000.0    	# min error
alpha     = float(alpha_max)   	# initial value of alpha parameter
ir        = 0.0                 # initial value of ir parameter ir
ne        = 1 

print " " 
print 'Record ' + str(n_rows) + ' Columns ' + str(n_cols)

# main loop
try:
  while ne <= nepoks: 
    if (ne % passo == 0):  # print running message when modulo division = zero
      min_err_txt = "%14.5f" % min_err    # format 8 integers and 3 decimals 
      alpha_txt  = "%12.5f" % alpha       # format 6 integers and 5 decimals 
      print ('Epoch ' + str(ne) + '   min err ' + min_err_txt + '   min epoch ' + 
          str(min_epok - 1) + "   alpha " + alpha_txt)
    if min_err < 1000000000.0: 
      nepokx += 1 
    if min_err > discrea and discrep > discrea and discrea > 0.0: 
      min_epok = ne               # current epoch (min) 
      min_err = discrea 
      # copy current grid to min grid
      gridm = copy.deepcopy(grid)       
      min_err_txt = "%12.3f" % min_err    # format 8 integers and 3 decimals 
      alpha_txt  = "%12.5f" % alpha       # format 6 integer and  5 decimals 
      print ('**** Epoch ' + str(ne - 1) + '       WITH MIN ERROR ' + min_err_txt + 
         "   alpha " + alpha_txt)
      
    # cheking the current value of alpha 
    if alpha > alpha_min:
      discrea = discrep 
      discrep = 0.0 
      # copy current grid to previous grid
      gridp = copy.deepcopy(grid)       
  
      # from the starting row to the ending row
      i = 0 
      while i < n_rows:
        iter += 1 
        # find the best grid coefficient
        ihit = 0 
        jhit = 0 
        dhit = 100000.0 
        igx = 0
        igy = 0
        while igx < nx: 
          igy = 0
          while igy < ny: 
            d = 0.0 
            neff = 0 
            k = 0
            arr_c = arr_r[i] 
            while k < m:   # update the sum of squared deviation of input 
                           # value from the grid coefficient
              ig = n.getcellindex((igx,igy,k))
              d = d + (arr_c[k+1] - grid[ig]) ** 2 
              k += 1 
            d = d / float(m)
            #  d = d / m 
            if d < dhit:
              dhit = d 
              ihit = int(igx)
              jhit = int(igy)
            igy += 1 
          igx += 1 
        # update iteration error
        discrep = discrep + dhit 
        # now we have the coordinates of the best grid coefficient
        ir = max(rmax * float(1001 - iter) / 1000.0 + 0.9999999999 , 1) 
        ir = int(ir) 
        # new alpha value to increase the radius of groups proximity 
        alpha = max(alpha_max * float(1 - ne * alpha_step) , alpha_min)
        # update the grid coefficients applying alpha parameter
        inn0 = int(ihit) - int(ir) 
        inn9 = int(ihit) + int(ir)
        jnn0 = int(jhit) - int(ir)
        jnn9 = int(jhit) + int(ir)
        while inn0 <= inn9: 
          jnn0 = int(jhit) - int(ir)
          while jnn0 <= jnn9:
            if not (inn0 < 0 or inn0 >= nx):
              if not (jnn0 < 0 or jnn0 >= ny): 
                arr_c = arr_r[i] 
                k = 0 
                while k < m:
                  ig = n.getcellindex((inn0,jnn0,k))
                  grid[ig] += alpha * (arr_c[k+1] - grid[ig])
                  k += 1 
            jnn0 += 1 
          inn0 += 1 
        i += 1 
    else: 
      print
      print "Min alpha reached " 
      print
      break   
    ne += 1 
except KeyboardInterrupt:
  print
  print "KeyboardInterrupt (Ctrl/C) " 
  print
  pass

# computing results
# grid = grid min 
grid = copy.deepcopy(gridm)       

# write min grid file 
arch_grid_file = open(arch_grid, 'w')
ii = 0 
while ii < nx:
  j = 0
  while j < ny:
    k = 0
    while k < m:
      ig = n.getcellindex((ii,j,k))
      arch_grid_file.write('%6i %s %.6i %s %.6i %s %14.7f %s' % (ii,' ', j ,' ', k,' ', grid[ig], "\n"))
      k += 1
    j += 1
  ii += 1
arch_grid_file.close()

# catalog input by min grid
ii = 0
while ii < n_rows: 
  ihit = 0 
  jhit = 0 
  dhit = 100000.0 
  # from 1 to numbers of groups
  ir = 0
  while ir < nx:         # from 1 to numbers of groups 
    jc = 0
    while jc < ny:       # from 1 to numbers of groups 
      d = 0.0 
      neff = 0 
      k = 0
      while k < n_cols:  # update the sum of squared deviation of input 
                         # value from the grid coefficient
        arr_c = arr_r[ii] 
        ig = n.getcellindex((ir,jc,k))
        d = d + (arr_c[k+1] - grid[ig]) ** 2 
        k += 1 
      d = d / m 
      if d < dhit:       # save the coordinates of the best coefficient 
        dhit = d 
        ihit = ir 
        jhit = jc 
      jc += 1 
    ir += 1 
  mtchx.append(ihit)
  mtchy.append(jhit) 
  ii += 1 

# write arch_catal file 
arch_catal_file = open(arch_catal, 'w')
ii = 0 
while ii < n_rows: 
  arch_catal_file.write("%.6i %s %.6i %s %.6i %s" % (ii, ' ', mtchx[ii], ' ', mtchy[ii], "\n")) 
  ii += 1 
arch_catal_file.close()

# matrix of statistics 
arr_cv   = []   	       # CV array of the Groups and Total
arr_med  = []      	       # means array of the Groups
riga_cv  = []          	       # CV row in arr_cv 
arr_col  = []          	       # group temporary array
arr_grsg = []         	       # input data array (normalized)
arr_grsg_c = []                # copy of arr_grsg (for file out sort) 

# input matrix sort in group sequence
ii = 0
ix = 0
while ii < n_rows: 
  ix += 1
  gr1 = str(mtchx[ii])
  if mtchx[ii] < 10:
    gr1 = '0' + str(mtchx[ii])
  sg1 = str(mtchy[ii])
  if mtchy[ii] < 10: 
    sg1 = '0' + str(mtchy[ii])
  riga_norm = arr_r[ii]
  im = 0
  riga_norm1 = []
  while im <= m: 
    riga_norm1.append(str(riga_norm[im]))
    im += 1
  riga_norm2 = " ".join(riga_norm1)  
  gr_sg_txt = "G_" + gr1 + "_" + sg1 + " " + str(ix) + " " + riga_norm2
  arr_grsg.append(gr_sg_txt) 
  ii += 1 
arr_grsg.sort()
ii = 0 
while ii < n_rows:
  arr_grsg_c.append(arr_grsg[ii]) 
  ii += 1 

# setup of arr_cv matrix 
num_gr = 0 
gruppo0 = "" 
ir = 0
while ir < n_rows:
  grsg_key = arr_grsg_c[ir].split()
  if not grsg_key[0] == gruppo0:
    gruppo0 = grsg_key[0]
    num_gr +=1 
    ic = 1 
    riga1 = [] 
    riga1.append(grsg_key[0]) 
    while ic <= m + 2:          # adding new columns for row mean and  n° of records
      riga1.append(0.0) 
      ic += 1 
    arr_cv.append(riga1)        # cv row 
  ir += 1 
riga1 = []
riga1.append("*Means*") 	# adding new row for cv mean
ic = 1
while ic <= m + 2:          	# adding new column for row mean and n° of records
  riga1.append(0.0) 
  ic += 1 
arr_cv.append(riga1)

def found(x):
  ir = 0
  while ir < len(arr_cv):
    linea_cv = arr_cv[ir]
    key_cv = linea_cv[0]
    if key_cv == x:
      return ir
    ir += 1

ir  = 0
irx = len(arr_grsg_c)
ic  = 3
linea_cv = arr_cv[0]
icx = len(linea_cv)
val_col = []

while ic < icx:
  ir = 0
  gruppo  = ""
  val_col = []
  while ir < irx:
    linea = arr_grsg_c[ir].split()
    if linea[0] == gruppo or gruppo == "":
      gruppo = linea[0] 
      val_col.append(float(linea[ic]))
    else:
      i_gruppo = found(gruppo)
      linea_cv = arr_cv[i_gruppo]
      media_v = abs(mean(val_col))
      if media_v == 0.0:
         media_v = 0.0000000001
      std_v = sd(val_col)
      cv_v  = std_v / media_v
      linea_cv[ic-2] = cv_v                      # cv value
      linea_cv[len(linea_cv)-1] = len(val_col)   # number of records
      val_col = []
      val_col.append(float(linea[ic]))
      gruppo = linea[0]
    ir += 1
  i_gruppo = found(gruppo)
  linea_cv = arr_cv[i_gruppo]
  media_v = abs(mean(val_col))
  if media_v == 0.0:
    media_v = 0.0000000001
  std_v = sd(val_col)
  cv_v  = std_v / media_v
  linea_cv[ic-2] = cv_v                          # cv value
  linea_cv[len(linea_cv)-1] = len(val_col)       # number of records
  ic += 1
ir  = 0
irx = len(arr_cv)
linea_cv = arr_cv[0]
icx = len(linea_cv) - 2
ic  = 1
num_rec1 = 0

while ir < irx:                                  # rows mean
  media_riga = 0.0
  ic = 1
  num_col1 = 0 
  linea_cv = arr_cv[ir]
  while ic < icx:
    media_riga += float(linea_cv[ic])
    num_col1 += 1
    ic += 1
  linea_cv[icx] = media_riga / num_col1
  num_rec1 += linea_cv[icx + 1]
  ir += 1
ir  = 0
ic  = 1

while ic < icx:                  # weighted mean of columns
  media_col = 0.0
  ir = 0
  num_rec1 = 0 
  while ir < irx - 1:
    linea_cv = arr_cv[ir]
    media_col = media_col + linea_cv[ic] * linea_cv[icx+1]  # linea_cv[icx+1] = number of records
    num_rec1 = num_rec1 + linea_cv[icx+1]
    ir += 1
  linea_cv = arr_cv[irx - 1]
  linea_cv[ic] = media_col / num_rec1
  ic += 1

# updating mean of the row
linea_cv = arr_cv[irx - 1]
linea_means = linea_cv[1:icx]
media_riga  = mean(linea_means)
linea_cv[icx] = media_riga        # Total mean
linea_cv[icx + 1] = num_rec1      # n° of records
cv_media_gen_after = str(media_riga)
cv_media_gen_after = cv_media_gen_after[0:6]  

# write cv  file 
testata_cv = testata
testata_cv[0] = "*Groups*"
testata_cv.append("*Mean*")
testata_cv.append("N_recs")
arch_cv_file = open(arch_cv, 'w')
ic = 0
while ic <= icx + 1:
  arch_cv_file.write('%s %s ' % (testata_cv[ic], " "*(9-len(testata_cv[ic]))))
  ic += 1
arch_cv_file.write('%s' % ('\n'))
ir = 0 
while ir < irx:
  ic = 0
  linea_cv = arr_cv[ir]
  while ic <= icx + 1:
    if ic == 0:
      arch_cv_file.write('%s %s ' % (linea_cv[0], "  "))
    else:
      if ic <= icx:
        arch_cv_file.write('%7.4f %s ' % (linea_cv[ic], "  "))
      else:
        arch_cv_file.write('%6i %s ' % (linea_cv[ic], "  "))
    ic += 1
  arch_cv_file.write('%s' % ("\n"))
  ir += 1
ic = 0

media_xcv = mean(xcv[1:icx])

while ic <= icx :   # print CV input (before catalogue)  
  if ic == 0:
    arch_cv_file.write('%s %s ' % ("*CVinp*", "  "))
  else:
    if ic < icx:
      arch_cv_file.write('%7.4f %s ' % (xcv[ic], "  "))
    else:
      arch_cv_file.write('%7.4f %s ' % (media_xcv, "  "))
      arch_cv_file.write('%6i %s ' % (linea_cv[ic+1], "  "))
  ic += 1
arch_cv_file.write('%s' % ("\n"))
#=========istruzioni aggiunte Roberto Bello 29/02/2012======================
#know_index = str(1.0 - float(cv_media_gen_after) / float(str_med_cv_gen))	
#know_index = know_index[0:6]
#arch_cv_file.write('%s %s %s' % ('*KIndex*   ', know_index, '\n'))
#=========fine istruzioni aggiunte da Roberto Bello 29/02/2012==============
arch_cv_file.close()

# writing out catalog file 
testata_cat1 = []
testata_cat1.append("*Group*")
arch_output_file = open(arch_output, 'w')
ic= 0
while ic < icx:
  testata_cat1.append(testata_cat[ic])
  ic += 1
ic= 0
while ic < len(testata_cat1):
  arch_output_file.write('%s %s ' % (testata_cat1[ic], " "*(15-len(testata_cat1[ic]))))
  ic += 1
arch_output_file.write('%s' % ("\n"))
index = 0 
while index < len(arr_orig):
  riga_orig = arr_orig[index]
  ic = 0
  while ic < len(riga_orig):
    if not(isinstance(riga_orig[ic],str)):
      riga_orig[ic] = str(riga_orig[ic])
    ic += 1   
  # place before 0 if gr / sg < 10 
  gr1 = str(mtchx[index])
  if mtchx[index] < 10:
    gr1 = '0' + str(mtchx[index])
  sg1 = str(mtchy[index])
  if mtchy[index] < 10: 
    sg1 = '0' + str(mtchy[index])
  arr_rig0 = "G_" + gr1 + "_" + sg1 + " "*8
  arch_output_file.write('%s ' % (arr_rig0))
  ic= 0
  while ic < len(riga_orig):
    arch_output_file.write('%s %s ' % (riga_orig[ic], " "*(15-len(riga_orig[ic]))))
    ic += 1
  arch_output_file.write('%s' % ("\n"))
  index += 1 
testata_cat1 = []
testata_cat1.append("*Group*")
testata_cat1.append("*RecNum*")
arch_sort_file = open(arch_sort, 'w')
ic= 0
while ic < icx:
  testata_cat1.append(testata_cat[ic])
  ic += 1
ic= 0
while ic < len(testata_cat1):
  arch_sort_file.write('%s %s ' % (testata_cat1[ic], " "*(15-len(testata_cat1[ic]))))
  ic += 1
arch_sort_file.write('%s' % ("\n"))
index = 0 
while index < len(arr_grsg_c):
  riga_grsg = arr_grsg_c[index].split()
  ic = 0
  while ic < len(riga_grsg):
    val_txt = riga_grsg[ic]
    val_txt = val_txt[0:13]
    arch_sort_file.write('%s %s ' % (val_txt, " "*(15-len(val_txt))))
    ic += 1
  if index < len(arr_grsg_c) - 1:
    arch_sort_file.write('%s' % ("\n"))
  index += 1 
arch_sort_file.close()

# writing out catalog and sorted file
arr_outsrt = []
index = 0
while index < len(arr_orig):
  riga_sort = []
  # place before 0 if gr / sg < 10 
  gr1 = str(mtchx[index])
  if mtchx[index] < 10:
    gr1 = '0' + str(mtchx[index])
  sg1 = str(mtchy[index])
  if mtchy[index] < 10: 
    sg1 = '0' + str(mtchy[index])
  riga_sort.append("G_" + gr1 + "_" + sg1)
  ic = 0
  riga_orig = arr_orig[index]
  while ic < len(riga_orig):
    val_riga = riga_orig[ic]
    riga_sort.append(val_riga)
    ic += 1
  arr_outsrt.append(riga_sort)
  index += 1

for line in arr_outsrt:
  line = "".join(line)  

arr_outsrt.sort()

testata_srt = []
testata_srt.append("*Group*")
arch_outsrt_file = open(arch_outsrt, 'w')
ic= 0
while ic < icx:
  testata_srt.append(testata_orig[ic])
  ic += 1
ic= 0
while ic < len(testata_srt):
  arch_outsrt_file.write('%s %s' % (testata_srt[ic], " "*(15-len(testata_srt[ic]))))
  ic += 1
arch_outsrt_file.write('%s' % ("\n"))
index = 0 
key_gruppo = "" 
while index < len(arr_outsrt):
  riga_sort = arr_outsrt[index] 
  index_c = 0 
  while index_c < len(riga_sort):
    if index_c == 0: 
      if riga_sort[0] != key_gruppo:
        # arch_outsrt_file.write('%s ' % ("\n"))
        key_gruppo = riga_sort[0] 
    valore = riga_sort[index_c] 
    arch_outsrt_file.write('%s %s' % (valore, " "*(15-len(valore))))
    index_c += 1 
  if index < len(arr_grsg_c) - 1:
    arch_outsrt_file.write('%s' % ("\n"))
  index += 1 
arch_outsrt_file.close()

print("###############################################################################")
print("# KB_CAT KNOWLEDGE DISCOVERY IN DATA MINING (CATALOG PROGRAM)                 #")
print("# by ROBERTO BELLO (COPYRIGHT MARCH 2011 ALL RIGHTS RESERVED)                 #")
print("# Language used: PYTHON                                                       #")
print("###############################################################################") 

arch_log_file = open(arch_log, 'w')
arch_log_file.write("%s %s" % ("############################################################################", "\n"))
arch_log_file.write("%s %s" % ("# KB_CAT KNOWLEDGE DISCOVERY IN DATA MINING (CATALOG PROGRAM)              #", "\n")) 
arch_log_file.write("%s %s" % ("# by ROBERTO BELLO (COPYRIGHT MARCH 2011 ALL RIGHTS RESERVED)              #", "\n")) 
arch_log_file.write("%s %s" % ("# Language used: PYTHON                     .                              #", "\n")) 
arch_log_file.write("%s %s" % ("############################################################################", "\n")) 
arch_log_file.write("%s %s %s" % ("Input File                                        -> ", file_input, "\n"))
arch_log_file.write("%s %s %s" % ("Numer of Groups (3 - 20)                          -> ", str(gruppi_num), "\n")) 
arch_log_file.write("%s %s %s" % ("Normalization (Max, Std, None)                    -> ", tipo_norm, "\n")) 
arch_log_file.write("%s %s %s" % ("Start Value of alpha (from 1.8 to 0.9)            -> ", str(alpha_max), "\n")) 
arch_log_file.write("%s %s %s" % ("End Value of alpha (from 0.5 to 0.0001)           -> ", str(alpha_min), "\n")) 
arch_log_file.write("%s %s %s" % ("Decreasing step of alpha (from 0.1 to 0.001)      -> ", str(alpha_step), "\n")) 
arch_log_file.write("%s"       % ("=========================OUTPUT=======================================================\n")) 
arch_log_file.write("%s %s %s" % ("Output File Catalog.original     ", arch_output, "\n"))
arch_log_file.write("%s %s %s" % ("Output File Catalog.sort         ", arch_outsrt, "\n")) 
arch_log_file.write("%s %s %s" % ("Output File Summary sort         ", arch_sort, "\n")) 
arch_log_file.write("%s %s %s" % ("Output File Matrix Catal.        ", arch_catal, "\n")) 
arch_log_file.write("%s %s %s" % ("Output File Means, STD, CV.      ", arch_medsd, "\n"))
arch_log_file.write("%s %s %s" % ("Output File CV of the Groups     ", arch_cv, "\n"))
arch_log_file.write("%s %s %s" % ("Output File Training Grid        ", arch_grid, "\n")) 
arch_log_file.write("%s %s %s" % ("Output File Run Parameters       ", arch_log, "\n"))
#=========istruzioni aggiunte Roberto Bello 29/02/2012======================
know_index = str(1.0 - float(cv_media_gen_after) / float(str_med_cv_gen))	
know_index = know_index[0:6]
arch_log_file.write('%s %s %s' % ('*KIndex*   ', know_index, '\n'))
#=========fine istruzioni aggiunte da Roberto Bello 29/02/2012==============

min_err_txt = "%12.3f" % min_err      # format 8 integer and 3 decimals 
alpha_txt  = "%12.5f" % alpha         # format 6 integer and 5 decimals 
alpha_min_txt = "%12.5f" % alpha_min  # format 6 integer and 5 decimals 

print 
if min_err == 1000000000.000:
  print("Oops! No result. Try again with new alpha parameters")
print 
print ("EPOCH " + str(min_epok -1) + "   WITH MIN ERROR " + min_err_txt + 
  " starting alpha " + alpha_min_txt + "   ending alpha " + alpha_txt + 
  " Iterations " + str(iter) + " Total Epochs " + str(ne - 1))
print 
print 'Output File Catalog.original ' + arch_output 
print 'Output File Catalog.sort     ' + arch_outsrt 
print 'Output File Summary sort     ' + arch_sort 
print 'Output File Matrix Catal.    ' + arch_catal 
print 'Output File Means, STD, CV.  ' + arch_medsd 
print 'Output File CV of the Groups ' + arch_cv 
print 'Output File Training Grid    ' + arch_grid 
print 'Output File Run Parameters   ' + arch_log 
print 'CV before Catalog            ' + str_med_cv_gen
print 'CV after Catalog             ' + cv_media_gen_after
know_index = str(1.0 - float(cv_media_gen_after) / float(str_med_cv_gen))
know_index = know_index[0:6]
print 'Knowledge Index              ' + know_index
print 

# Elapsed time
t1 = datetime.datetime.now()
elapsed_time = t1 - t0
print "Elapsed time (seconds)   :   " + str(elapsed_time.seconds)
print 
