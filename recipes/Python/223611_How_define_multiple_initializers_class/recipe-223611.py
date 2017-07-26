# example class with ordinary constructor and class-level factory method
class Color:
  """class for specifying colors while drawing BitMap elements"""
  def __init__( self, r=0, g=0, b=0 ):
    self.red = r
    self.grn = g
    self.blu = b
    
  def __str__( self ):
    return "R:%d G:%d B:%d" % (self.red, self.grn, self.blu )
  
  def toLong( self ):
    return ( long(self.blu)       ) + \
           ( long(self.grn) <<  8 ) + \
           ( long(self.red) << 16 )

  def fromLong( cls, lng ):
    blu = lng & 0xff
    lng = lng >> 8
    grn = lng & 0xff
    lng = lng >> 8
    red = lng & 0xff
    return cls( red, grn, blu )
  fromLong = classmethod( fromLong )


c = Color( 255, 0, 0 ) # red
print c
colorInt = c.toLong()
print colorInt
print Color.fromLong( colorInt )
