class tkMath( object ):
   PIXELS_PER_INCH    = 0
   PIXELS_PER_CM      = 0
   PIXELS_PER_MM      = 0
   PIXELS_PER_POINT   = 0
   
   @staticmethod
   def setup( root ):
      '''Must be called before any of the methods are used to initialize
      the conversion constants.'''
      tkMath.PIXELS_PER_INCH  = root.winfo_fpixels( '1i' )
      tkMath.PIXELS_PER_CM    = root.winfo_fpixels( '1c' )
      tkMath.PIXELS_PER_MM    = root.winfo_fpixels( '1m' )
      tkMath.PIXELS_PER_POINT = root.winfo_fpixels( '1p' )
   
   @staticmethod
   def pixelsToInches( pixels ):
      '''Convert pixels (python float or int) to inches.'''
      return pixels / tkMath.PIXELS_PER_INCH
   
   @staticmethod
   def pixelsToCM( pixels ):
      '''Convert pixels (python float or int) to centimeters.'''
      return pixels / tkMath.PIXELS_PER_CM
   
   @staticmethod
   def pixelsToMM( pixels ):
      '''Convert pixels (python float or int) to millimeters.'''
      return pixels / tkMath.PIXELS_PER_MM
   
   @staticmethod
   def pixelsToPoints( pixels ):
      '''Convert pixels (python float or int) to points.'''
      return pixels / tkMath.PIXELS_PER_POINT
   
   @staticmethod
   def inchesToPixels( inches ):
      '''Convert inches (python float or int) to pixels.'''
      return inches * tkMath.PIXELS_PER_INCH
   
   @staticmethod
   def cmToPixels( cm ):
      '''Convert centimeters (python float or int) to pixels.'''
      return cm * tkMath.PIXELS_PER_CM

   def mmToPixels( mm ):
      '''Convert millimeters (python float or int) to pixels.'''
      return mm * tkMath.PIXELS_PER_MM

   def pointsToPixels( points ):
      '''Convert points (python float or int) to pixels.'''
      return points * tkMath.PIXELS_PER_POINTS

   @staticmethod
   def toPixels( tkCoord ):
      '''Convenience function for inches, cm, mm and pointsToPixels().
      Convert a tkCoord (string appended by 'i', 'c', 'm' or 'p') to pixels.'''
      if isinstance( tkCoord, str ):
         if tkCoord[-1] == 'i':
            return tkMath.inchesToPixels( float(tkCoord[:-1]) )
         elif tkCoord[-1] == 'c':
            return tkMath.cmToPixels( float(tkCoord[:-1]) )
         elif tkCoord[-1] == 'm':
            return tkMath.mmToPixels( float(tkCoord[:-1]) )
         elif tkCoord[-1] == 'p':
            return tkMath.pointsToPixels( float(tkCoord[:-1]) )
         else:
            return float(tkCoord)
      else:
         return tkCoord

   @staticmethod
   def compare( coord1, coord2 ):
      '''Compare two tk measures -- they need not be in the same units.'''
      return tkMath.coordToPixels(coord1) - tkMath.coordToPixels(coord2)

   @staticmethod
   def add( coord1, coord2 ):
      '''Add two tk measures -- they need not be in the same units.'''
      return tkMath.coordToPixels(coord1) + tkMath.coordToPixels(coord2)
   
   @staticmethod
   def sub( coord1, coord2 ):
      '''Subtract two tk measures -- they need not be in the same units.'''
      return tkMath.coordToPixels(coord1) - tkMath.coordToPixels(coord2)
   
   @staticmethod
   def tkPolar( x1, y1, x2, y2 ):
      '''Calculate the direction (in radians, 3 o'clock is 0,
      down is 1/2 PI, etc.) and distance (in pixels) between to points.
      All arguments should be in the same units (python float or int).
      The result is in the same units as the arguments.'''
      import math
      deltaX = math.fabs( x1 - x2 )
      deltaY = math.fabs( y1 - y2 )

      direction = math.atan2( deltaY, deltaX )
      distance  = math.sqrt( math.pow(deltaX, 2) + math.pow(deltaY, 2) )

      return direction, distance

   @staticmethod
   def tkCartesian( x, y, direction, distance ):
      '''Complementary to tkPolar().  Given a x,y point, direction in
      radians (0 is at 3 o'clock, 1/2 PI is straight down, etc.) and a
      distance (all as python float or int).  This function returns
      the x and y of the end-point.'''
      import math
      deltaX = distance * math.cos( direction )
      deltaY = distance * math.sin( direction )
      
      return x + deltaX, y + deltaY
