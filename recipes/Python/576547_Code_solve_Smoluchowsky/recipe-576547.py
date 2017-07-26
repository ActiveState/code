#! /usr/bin/env python
import scipy as s
import pylab as p
import scipy.integrate as si
from scipy import stats #I need this module for the linear fit
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os



def mail(to, subject, text, attach):
   msg = MIMEMultipart()

   msg['From'] = gmail_user
   msg['To'] = to
   msg['Subject'] = subject

   msg.attach(MIMEText(text))

   part = MIMEBase('application', 'octet-stream')
   part.set_payload(open(attach, 'rb').read())
   Encoders.encode_base64(part)
   part.add_header('Content-Disposition',
           'attachment; filename="%s"' % os.path.basename(attach))
   msg.attach(part)

   mailServer = smtplib.SMTP("smtp.gmail.com", 587)
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.ehlo()
   mailServer.login(gmail_user, gmail_pwd)
   mailServer.sendmail(gmail_user, to, msg.as_string())
   # Should be mailServer.quit(), but that crashes...
   mailServer.close()


def Brow_ker_cont_optim(Vlist):
	kern_mat=2.*k_B*T_0/(3.*mu)*(Vlist[:,s.newaxis]**(1./3.)+\
	Vlist[s.newaxis,:]**(1./3.))**2./ \
	(Vlist[:,s.newaxis]**(1./3.)*Vlist[s.newaxis,:]**(1./3.))
	return kern_mat
	



def coupling_optim_garrick(y,t):
	creation=s.zeros(n_bin)
	destruction=s.zeros(n_bin)
	#now I try to rewrite this in a more optimized way
	destruction = -s.dot(s.transpose(kernel),y)*y #much more concise way to express\
	#the destruction of k-mers 
	
	for k in xrange(n_bin):
		kyn = (kernel*f_garrick[:,:,k])*y[:,s.newaxis]*y[s.newaxis,:]
		creation[k] = s.sum(kyn)
	creation=0.5*creation
	out=creation+destruction
	return out



#Now I work with the function for espressing smoluchowski equation when a uniform grid is used

def coupling_optim(y,t):
	creation=s.zeros(n_bin)
	destruction=s.zeros(n_bin)
	#now I try to rewrite this in a more optimized way
	destruction = -s.dot(s.transpose(kernel),y)*y #much more concise way to express\
	#the destruction of k-mers 
	kyn = kernel*y[:,s.newaxis]*y[s.newaxis,:]
	for k in xrange(n_bin):
		creation[k] = s.sum(kyn[s.arange(k),k-s.arange(k)-1])
	creation=0.5*creation
	out=creation+destruction
	return out


#Now I go for the optimal optimization of the chi_{i,j,k} coefficients used by Garrick for
# dealing with a non-uniform grid. 

def mycount_garrick(V):
	f=s.zeros((n_bin, n_bin, n_bin))
	Vsum=V[:,s.newaxis]+V[s.newaxis,:] # matrix with the sum of the volumes in the bins
	for k in xrange(1,(n_bin-1)):
		f[:,:,k]=s.where((Vsum<=V[k+1]) & (Vsum>=V[k]), (V[k+1]-Vsum)/(V[k+1]-V[k]),\
		f[:,:,k] )
		f[:,:,k]=s.where((Vsum<=V[k]) & (Vsum>=V[k-1]),(Vsum-V[k-1])/(V[k]-V[k-1]),\
		f[:,:,k])
	
	return f



def total_concentration(number_mat, box_volume):
	number= s.sum(number_mat,axis=1)*box_volume
	return number

def total_mass_conservation(number_mat, vol_grid,box_volume):
	ini_mass=s.dot(number_mat[0,:],vol_grid)*box_volume
	fin_mass=s.dot(number_mat[-1,:],vol_grid)*box_volume
	mass_conservation=(ini_mass-fin_mass)/ini_mass

	results=s.array([ini_mass,fin_mass,mass_conservation])
	return results

	

def fitting_stat(x,y):
    slope, intercept, r, prob2, see = stats.linregress(x,y)

    if (len(x)>2):
        
        see=see*s.sqrt(len(x)/(len(x)-2.))

        mx = x.mean()
        sx2 = ((x-mx)**2).sum()
        sd_intercept = see * s.sqrt(1./len(x) + mx*mx/sx2)
        sd_slope = see * s.sqrt(1./sx2)

    results=s.zeros(5)

    results[0]=slope
    results[1]=intercept
    results[2]=r
    if (len(x)>2):
        results[3]=sd_slope
        results[4]=sd_intercept

    return results



#Now a list of the physical parameters needed to carry out the calculation

n_mon=5000 #total number of monomers

initial_density=0.01 #monomer density in the box

box_vol=n_mon/initial_density  #volume of the box containing the monomers

r_mon=0.5 #radius of each monomer

v_mono=4./3.*s.pi*r_mon**3. #volume of each monomer





beta=1. #cluster-monomer 1/tau
k_B=1. #in these units
T_0=0.5 #temperature of the system
m_mon=1. #monomer mass in these units
sigma=1. #monomer diameter
mu=(m_mon*beta)/(3.*s.pi*sigma) # fluid viscosity

t=s.linspace(0.,1000.,1001) # choose time grid for time evolution

#Specify the bin structure you want to use

linear =1  #linear ==1---> use a linear bin structure and solve smoluchowski equation in standard form
           #linear !1---> use a non-linear (log-spaced) bin structure and solve smoluchowski equation
	   # using the splitting operator


k_max=1000  #maximum number of monomers I consider in a k_mer

n_bin=200  # to be used only if a non-linear bin structure is used



send_email=1  #tells whether you want to send an email with an attached
              # file 


# variables for sending emails


gmail_user = "someaccount@gmail.com"     #modify this using the account name and password of
                                         #your own gmail account
gmail_pwd = "password"

mailto = "robert.h.schingler@nasa.gov"

mailtitle = "The job you submitted is done"

mailtext = "This is an automatically-generated email, please do not reply"



if (linear==1):

   mailattachment="evolution_number_of_monomers_linear_binning.pdf"
else:
   mailattachment="evolution_number_of_monomers_nonlinear_binning.pdf"




if (linear == 1):
	k_list=s.linspace(1., k_max, k_max) #list of number I use to label each bin, i.e. size of the
	#corresponding monomer
	vol_grid=k_list*v_mono #volume of the particle in the k-th bin
	n_bin=len(k_list) #overwrite the number of bins
	
elif (linear !=1):
	k_list=s.logspace(s.log10(1.), s.log10(k_max),n_bin)  
	vol_grid=k_list*v_mono #volume of the particle in the k-th bin (this time the volume list is
	                         #nonlinear)






if (linear !=1): #calculate the splitting operator on the non-uniform grid
	f_garrick=mycount_garrick(vol_grid) #I calculate the splitting operator on the grid

#generate initial condition [monodisperse aerosol]
y0=s.zeros(n_bin)
y0[0]=initial_density  #initial state (monodisperse aerosol)



#Generate the kernel matrix

kernel=Brow_ker_cont_optim(vol_grid)



if (linear==1):
	solution = si.odeint(coupling_optim, y0, \
		   t,printmessg=1,rtol=1e-10,atol=1e-10)

elif (linear!=1):

	solution = si.odeint(coupling_optim_garrick, y0, \
		   t,printmessg=1,rtol=1e-10,atol=1e-10)



total_monomers=total_concentration(solution, box_vol)
#now save the total number of monomers and the time in two separate files

if (linear==1): 

	p.save("number_monomers_linear_binning.dat", total_monomers)

elif (linear !=1):

	p.save("number_monomers_nonlinear_binning.dat", total_monomers)


p.save("time.dat", t)


#check the quality of the simulation by testing mass conservation

mass_tests=total_mass_conservation(solution, vol_grid,box_vol)

print "initial and final total mass in the box are", mass_tests[0], mass_tests[1] ,"respectively"

print "mass is conserved up to ", mass_tests[2]*100., "percent"

#finally, perform some basic statistical analysis (fit decay of total number of clusters to a power-law)

sel_late=s.where(t>800.)

results=fitting_stat(s.log(t[sel_late]),s.log(total_monomers[sel_late]))

power_decay=results[0]

print "the exponent of the power-law decay [the theoretical value is -1] is, ", power_decay

#finally, plot the results

fig = p.figure()
axes = fig.gca()


axes.plot(t,total_monomers,"ro",linewidth=2.)
p.xlabel('Time')
p.ylabel('Total number of monomers')
p.title('Evolution of the total number of monomers')
p.grid(True)
if (linear ==1 ):
	fig_name="evolution_number_of_monomers_linear_binning.pdf"
elif (linear !=1):
	fig_name="evolution_number_of_monomers_nonlinear_binning.pdf"

p.savefig(fig_name)

p.clf()








#Now send one of the generated plots automatically by email


#NB: this will not work unless one really inputs its email login details

mail(mailto,mailtitle, mailtext,mailattachment)





print "Calculation ended."
