# Author: Anand Patil
# License: MIT License

import matplotlib.pyplot as pl
import numpy as np

def symmetric(sorted_streams, stream_bounds):
    """Symmetric baseline"""
    lb, ub = np.min(stream_bounds[:,0,:],axis=0), np.max(stream_bounds[:,1,:],axis=0)
    return .5*(lb+ub)
def pos_only(sorted_streams, stream_bounds):
    """Lumps will only be positive"""
    lb, ub = np.min(stream_bounds[:,0,:],axis=0), np.max(stream_bounds[:,1,:],axis=0)
    return lb
def zero(sorted_streams, stream_bounds):
    """Zero baseline"""
    return np.zeros(stream_bounds.shape[2])
def min_weighted_wiggles(sorted_streams, stream_bounds):
    """Baseline recommended by Byron and Wattenberg"""
    lb, ub = np.min(stream_bounds[:,0,:],axis=0), np.max(stream_bounds[:,1,:],axis=0)
    weight = ub-lb
    
    sorted_streams = np.abs(sorted_streams)
    for i in xrange(len(sorted_streams)):
        sorted_streams[i,:] *= (-1)**i
    cusum_f = np.vstack((np.zeros(sorted_streams.shape[1]),
                        np.cumsum(sorted_streams[:-1,:], axis=0)))
    f_prime = np.diff(sorted_streams, axis=1)
    cusum_f_prime = np.diff(cusum_f, axis=1)
    g_prime = np.hstack(([0],-np.sum((f_prime*.5  + cusum_f_prime)*sorted_streams[:,1:],axis=0) / weight[1:]))
    g_prime[np.where(weight==0)] = 0
    g = np.cumsum(g_prime)
    
    return g
    

def stacked_graph(streams, cmap=pl.cm.bone, color_seq='linear', baseline_fn=min_weighted_wiggles):
    """
    Produces stacked graphs using matplotlib.
    
    Reference: 'Stacked graphs- geometry & aesthetics' by Byron and Wattenberg
    http://www.leebyron.com/else/streamgraph/download.php?file=stackedgraphs_byron_wattenberg.pdf
    
    Parameters:
      - streams: A list of time-series of positive values. Each element must be of the same length.
      - cmap: A matplotlib color map. Defaults to 'bone'.
      - colo_seq: 'linear' or 'random'.
      - baseline_fn: Current options are symmetric, pos_only, zero and min_weighted_wiggles.
    """
    # Sort by onset times
    onset_times = [np.where(np.abs(stream)>0)[0][0] for stream in streams]
    order = np.argsort(onset_times)
    streams = np.asarray(streams)
    sorted_streams = streams[order]
    
    t = np.arange(streams.shape[1])
    
    # Establish bounds
    stream_bounds = [np.vstack((np.zeros(streams.shape[1]), sorted_streams[0])),
                    np.vstack((-sorted_streams[1], (np.zeros(streams.shape[1]))))]
    side = -1
    for stream in sorted_streams[2:]:
        side *= -1
        if side==1:
            stream_bounds.append(np.vstack((stream_bounds[-2][1], stream_bounds[-2][1]+stream)))
        else:
            stream_bounds.append(np.vstack((stream_bounds[-2][0]-stream, stream_bounds[-2][0])))
            
    stream_bounds = np.array(stream_bounds)
    
    # Compute baseline
    baseline = baseline_fn(sorted_streams, stream_bounds)
    
    # Choose colors
    t_poly = np.hstack((t,t[::-1]))
    if color_seq=='linear':
        colors = np.linspace(0,1,streams.shape[1])
    elif color_seq=='random':
        colors = np.random.random(size=streams.shape[1])
    else:
        raise ValueError, 'Color sequence %s unrecognized'%color_seq
    
    # Plot    
    pl.axis('off')        
    for i in xrange(len(stream_bounds)):
        bound = stream_bounds[i]
        color = cmap(colors[i])
        pl.fill(t_poly, np.hstack((bound[0]-baseline,(bound[1]-baseline)[::-1])), facecolor=color, linewidth=0.,edgecolor='none')
        
        
# Demo
if __name__ == '__main__':
    pl.clf()
    N_dsets = 50
    T = 100
    amp = 1
    fade = .15
    dsets = []
    for i in xrange(N_dsets):
        this_dset = np.zeros(T)
        t_onset = np.random.randint(.9*T)-T/3
        if t_onset >= 0:   
            remaining_t = np.arange(T-t_onset)     
        else:
            remaining_t = np.arange(T)-t_onset
        this_dset[max(t_onset,0):]=np.exp(-.15*np.random.gamma(10,.1)*remaining_t)\
                            * remaining_t * np.random.gamma(6,.2)# * np.cos(-fade*remaining_t*np.random.gamma(10,.1))**2
        dsets.append(this_dset)
    stacked_graph(dsets, baseline_fn = min_weighted_wiggles, color_seq='random')
