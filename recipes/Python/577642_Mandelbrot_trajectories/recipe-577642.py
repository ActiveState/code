"""An interactive graph to plot the trajectory of points on and off the mandelbrot
set. Illustrates the use of sliders in matplotlib"""
import pylab
from matplotlib.widgets import Slider

def compute_trajectory(x0, y0, set_boundary = 2, n_iters = 100):
  """Take the fragment and compute a further n_iters iterations for each element
  that has not exceeded the bound. Also indicate if we are inside or outside the
  mandelbrot set"""
  
  set = True
  C = complex(x0, y0)
  Z = pylab.ones(n_iters,'complex')*C
  for n in range(n_iters-1):
    if abs(Z[n]) > set_boundary:
      Z[n+1:] = Z[n]
      set = False
      break
    Z[n+1] = Z[n]*Z[n] + C 
        
  return Z, set

axcolor = 'lightgoldenrodyellow'
ax_x = pylab.axes([0.1, 0.04, 0.8, 0.03], axisbg=axcolor)
ax_y  = pylab.axes([0.1, 0.01, 0.8, 0.03], axisbg=axcolor)
sx = Slider(ax_x, 'x', -1.0, 1.0, valinit=0)
sy = Slider(ax_y, 'y', -1.0, 1.0, valinit=0)
 
ax_plot = pylab.axes([0.12, 0.12, 0.85, 0.85])
Z,s = compute_trajectory(0,0)
l, = pylab.plot(Z.real, Z.imag,'.-') #Ain't that cool?
st, = pylab.plot(Z[0].real, Z[0].imag,'ok')
pylab.setp(ax_plot,'xlim',[-1,1], 'ylim', [-1,1])
#pylab.axis('scaled')

m_set = [[0],[0]]
ms, = pylab.plot(m_set[0], m_set[1],'k.')


def update(val):
  x = sx.val
  y = sy.val
  Z, set = compute_trajectory(x,y)
  l.set_xdata(Z.real)
  l.set_ydata(Z.imag)
  st.set_xdata(Z[0].real)
  st.set_ydata(Z[0].imag)  
  if set:
    m_set[0] += [x]
    m_set[1] += [y]
  ms.set_xdata(m_set[0])
  ms.set_ydata(m_set[1])  
  pylab.draw()
  
sx.on_changed(update)
sy.on_changed(update)
