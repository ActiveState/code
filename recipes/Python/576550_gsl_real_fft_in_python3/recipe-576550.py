'''
    provide a simple python3 interface to the gsl_fft_real_transform function
'''

import sys
import itertools
from gsl_setup import *

def grouper(n, iterable, fillvalue=None):
    # http://docs.python.org/dev/3.0/library/itertools.html#module-itertools
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return itertools.zip_longest(fillvalue=fillvalue, *args)

real_workspace_alloc = setup(
    gsl.gsl_fft_real_workspace_alloc,[c_ulong,],c_void_p)
real_wavetable_alloc = setup(
    gsl.gsl_fft_real_wavetable_alloc,[c_ulong,],c_void_p)
real_workspace_free =setup(gsl.gsl_fft_real_workspace_free ,[c_void_p,])
real_wavetable_free =setup(gsl.gsl_fft_real_wavetable_free ,[c_void_p,])

real_transform = setup(gsl.gsl_fft_real_transform,
                       [c_void_p,c_ulong,c_ulong,c_void_p,c_void_p],)


class Real_FFT:

    '''
        returns the complex values of the real transform of the real data.
        return value[0] describes the offset,
                    [1] is amplitude of term for wavelength = data length
                    etceteras
                    [-1] amp of wavelength = twice sample distance
    '''

    def __init__(self):
        self.n = 0

    def __call__(self,data):
        if len(data) < 2:
            if 1 == len(data):
                return data[:]
            return []
        if len(data) != self.n:
            self.__del__()
            self.n = len(data)
            size = c_ulong(self.n)
            self.workspace = real_workspace_alloc(size)
            self.wavetable = real_wavetable_alloc(size)
        a = array('d',data)       # need a copy of the data
        real_transform(ADDRESS(a),1,self.n,self.wavetable,self.workspace)
        rv = [complex(a[0]),]
        rv.extend(itertools.starmap(complex,grouper(2,a[1:],fillvalue=0)))
        return rv

    def __del__(self):
        if self.n:
            try:
                real_workspace_free(self.workspace)
                real_wavetable_free(self.wavetable)
            except AttributeError:
                print('Attribute error while freeing FFT auxiliary storage',
                      file=sys.stderr)
            except:
                print('error freeing FFT auxiliary storage',
                      file=sys.stderr)

    def produce_frequency(self,*,samples=None,sample_interval=None,sample_rate=None,total_length=None):
        '''
            return the frequency grid based on actual sizes (default sample_interval=1).
        '''
        n = samples or self.n
        if not n:
            return array('d')
        args_specified = 3 - ((not sample_interval)+(not sample_rate)+(not total_length))
        if 1 < args_specified:
            raise TypeError('specify at most one of [sample_rate, total_length, sample_interval]')
        if 0 == args_specified:
            L = n
        elif sample_interval:
            L = n*sample_interval
        elif sample_rate:
            L = n/sample_rate
        else:
            L = total_length
        return as_array(waves/L for waves in range(1+n//2))
            
    def produce_period(self,*args,**kwargs):
        '''
            return the period grid based on actual sizes.
            frequency of zero --> period 0.  what else to do?
        '''
        f2T = self.produce_frequency(*args,**kwargs)
        for i in range(1,len(f2T)):
            f2T[i] = 1/f2T[i]
        return f2T

real_fft = Real_FFT()

def magnitude(a):
    return [abs(b) for b in a]

def phase(a):
    return [phase(b) for b in a]
