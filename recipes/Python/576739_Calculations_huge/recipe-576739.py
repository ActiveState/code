#/usr/bin/env python
import numpy as np
import sys
#-----------------------------------------------------------------------------#
def attrs_from_locals(instance):
    """
    Stolen and shortened from http://code.activestate.com/recipes/286185/
    Sets every local variable mentioned so far as an instance attribute.
    """
    for key, value in sys._getframe(1).f_locals.items():
        if key != 'self':
            setattr(instance, key, value)
#-----------------------------------------------------------------------------#
class Hard_calc(object):
    def __init__(self, filepath, m_shape, m_dtype='float64', 
                 chunk_size=512*1024**2):
        """
        Use this for calculations on huge arrays that won't fit into memory.  
        
        It makes use of the numpy.memmap-class and does calculations 
        chunk-wise. "chunk_size" determines how much Bytes of the memmap-array 
        are hold in memory.
        """
        m_array = np.memmap(filepath, mode='w+', dtype=m_dtype, shape=m_shape)
        row_size = np.prod(m_array.shape[1:]) * m_array.dtype.itemsize
        step_length = \
            int(chunk_size / row_size) if chunk_size > row_size else 1
        attrs_from_locals(self)
    #-------------------------------------------------------------------------#
    @staticmethod
    def operation():
        raise AttributeError, \
            "Append your own operation-method, otherwise I have nothing to do."
    #-------------------------------------------------------------------------#
    def __call__(self, *o_args, **o_kwds):
        """
        Applies "operation". Make sure that method is present.
        Called without "o_args" the memmap-array is used as a parameter for
        "operation".
        """
        o_args = [self.m_array] if len(o_args) == 0 else o_args
        ii = 0
        while ii != None:
            ii_new = ii + self.step_length if \
                ii + self.step_length < len(self.m_array) else None
            sliced_o_args = [o_arg[ii:ii_new] for o_arg in o_args]
            self.m_array[ii:ii_new] = self.operation(*sliced_o_args, **o_kwds)
            del self.m_array  # writes to file and frees memory
            self.m_array = np.memmap(self.filepath, mode='r+', 
                                     dtype=self.m_dtype, shape=self.m_shape)
            ii = ii_new
        return self.m_array
#-----------------------------------------------------------------------------#
if __name__ == "__main__":
    """
    The generation of sample-data here is not very fitting: The complete data 
    is allready in the memory to begin with.  Imagine you opened a netCDF-, 
    grib- or memmap-file and u and v are just references to data stored on the
    harddisk.
    """
    u = np.random.rand(100, 100, 100)
    v = np.random.rand(100, 100, 100)
    Energy = Hard_calc("energy", u.shape, m_dtype='float', chunk_size=1024**2)
    
    Energy.operation = lambda u, v: u**2 + v**2
    wind_energy = Energy(u, v)
    Energy.operation = np.sqrt
    horizontal_velocity = Energy()
