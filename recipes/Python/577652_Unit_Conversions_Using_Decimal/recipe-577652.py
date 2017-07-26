"""
This recipe generates a module convert.py and convertTest.txt which is used
to test conversion.py when it is run.

conversion.py is built from the table defining the unit conversions
  * uses the decimal module as a base class and unit types are class properties.
  * provides exact decimal representation
  * control over precision
  * control over rounding to meet legal or regulatory requirements
  * tracking of significant decimal places
  * results match calculations done by hand
  
conversion.py supplies the following classes:
    Distance
    Area
    Volumn
    Time
    Velocity
    Acceleration
    Mass
    Force
    Weight
    Pressure
    Frequency
    Power
    Temperature
    
"""

from decimal import *

header = """
  conversion.py
  
  Unit Conversion
  Dave Bailey
  4/10/2011
 
  The conversion.py module uses Decimal from the decimal module as the base class
  decimal is based on the General Decimal Arithmetic Specification
  IEEE standard 854-1987
  conversion provides:
     exact decimal representation
     control over precision,
     control over rounding to meet legal or regulatory requirements,
     tracking of significant decimal places
     results match calculations done by hand. 

"""
examples = """
-- Examples:
>>> d = Distance(0.0)
>>> d.mi = 1.0
>>> print 'ft -> mile %.3f, %f, %s, %r' % (d.ft,d.ft,d.ft,d.ft)
ft -> mile 5280.000, 5280.000000, 5280.000000000000000000000000, Decimal('5280.000000000000000000000000')
>>> getcontext().prec = 28
>>> d = Distance(0.0)
>>> d.mi = 1.0
>>> print 'ft -> mile %.3f, %f, %s, %r' % (d.ft,d.ft,d.ft,d.ft)
ft -> mile 5280.000, 5280.000000, 5280.000000000000000000000000, Decimal('5280.000000000000000000000000')

>>> getcontext().prec = 52
>>> d = Distance(0.0)
>>> d.mi = 1.0
>>> print 'ft -> mile %.3f, %f, %s, %r' % (d.ft,d.ft,d.ft,d.ft)
ft -> mile 5280.000, 5280.000000, 5279.999999999999999999999999588007935999999954845670, Decimal('5279.999999999999999999999999588007935999999954845670')

>>> getcontext().prec = 28
>>> with localcontext() as ctx:
...     getcontext().prec = 52
...     d = Distance(0.0)
...     d.mi = 1.0
...     print 'ft -> mile %.3f, %f, %s, %r' % (d.ft,d.ft,d.ft,d.ft)
ft -> mile 5280.000, 5280.000000, 5279.999999999999999999999999588007935999999954845670, Decimal('5279.999999999999999999999999588007935999999954845670')

>>> getcontext().prec
28
>>> d.ft
Decimal('5280.000000000000000000000000')

>>> d0 = Distance('.10')
>>> d = Distance(d0+d0+d0-Decimal('.30'))
>>> '%r' % d.m
"Decimal('0.00')"

>>> d = Distance(.10 + .10 + .10 - .30)
>>> '%r' % d.m
"Decimal('5.5511151231257827021181583404541015625E-17')"

>>> d.m = '1.0'
>>> d.ft
Decimal('3.28083989501312300000')
>>> d.inch
Decimal('39.370078740157476000000')
>>> d.m = 1.0
>>> d.ft
Decimal('3.2808398950131230000')
>>> d.inch
Decimal('39.37007874015747600000')
>>> print d
1 meters (m)
0.000621371 miles (mi)
1.09361 yard (yd)
3.28084 feet (ft)
39.3701 inch (inch)
0.001 kilometers (km)
100 centimeters (cm)
1000 millimeters (mm)
1e+09 nanometer (nm)
>>> d
Decimal('1') meters (m)
Decimal('0.0006213711922373339015151515152') miles (mi)
Decimal('1.093613298337707666666666667') yard (yd)
Decimal('3.2808398950131230000') feet (ft)
Decimal('39.37007874015747600000') inch (inch)
Decimal('0.0010') kilometers (km)
Decimal('1.0E+2') centimeters (cm)
Decimal('1.0E+3') millimeters (mm)
Decimal('1.0E+9') nanometer (nm)

# distance = vt+.5at**2
>>> v = Velocity(49.0332501432)
>>> a = Acceleration(-9.80665002864) # gravity
>>> t = Time(0.0)
>>> print 'initial velocity = %f mps = %f fps' % (v.mps,v.fps)
initial velocity = 49.033250 mps = 160.870243 fps
>>> for sec in range(20):
...     t.sec = sec
...     d = v*t + Decimal(.5)*a*t**2
...     height = Distance(d)
...     if height < 0: break
...     print 't',t.sec,'height',height.m,'m',height.ft,'ft'
t 0 height 0E-47 m 0E-66 ft
t 1 height 44.12992512888000007365008059 m 144.7832189267716379167004149 ft
t 2 height 78.45320022912000013093347661 m 257.3923892031495785185785154 ft
t 3 height 102.9698253007200001718501880 m 337.8275108291338218056343013 ft
t 4 height 117.6798003436800001964002149 m 386.0885838047243677778677731 ft
t 5 height 122.5831253580000002045835572 m 402.1756081299212164352789303 ft
t 6 height 117.6798003436800001964002149 m 386.0885838047243677778677731 ft
t 7 height 102.9698253007200001718501881 m 337.8275108291338218056343016 ft
t 8 height 78.4532002291200001309334767 m 257.3923892031495785185785157 ft
t 9 height 44.1299251288800000736500806 m 144.7832189267716379167004149 ft
t 10 height 0E-25 m 0E-44 ft

from decimal import *

"""

constants = """
from decimal import *

GRAVITY = Decimal('9.80665002864') # m/s2
FT_IN_MI = Decimal('5280.0')
FT_IN_M = Decimal('3.2808398950131230000') 
FT_IN_YD = Decimal('3.0')
INCH_IN_FT = Decimal('12.0')

MI_IN_M = FT_IN_M / FT_IN_MI
YD_IN_M = FT_IN_M / FT_IN_YD
INCH_IN_M = FT_IN_M * INCH_IN_FT
KM_IN_M = Decimal('1.0e-3')
CM_IN_M = Decimal('1.0e2')
MM_IN_M = Decimal('1.0e3')
NM_IN_M = Decimal('1.0e9')

SEC_IN_MIN = Decimal('60.0')
MIN_IN_HR = Decimal('60.0')
DAY_IN_WK = Decimal('7.0')
HR_IN_DAY = Decimal('24.0')
DAY_IN_YR = Decimal('365.24218967')

HR_IN_SEC = Decimal('1.0')/(SEC_IN_MIN * MIN_IN_HR)

G_IN_KG = Decimal('1.0e3')
LB_IN_NEWTON = Decimal('.224808942911188')
OZ_IN_G = Decimal('0.0352739619000')
OZ_IN_LB = Decimal('16.0')
W_IN_HP = Decimal('745.699872')
"""


tables = [
    [
    ["Distance","meters"],
    ["meters","m","Decimal(self)","self._update(Decimal(value))"],
    ["miles","mi","Decimal(self) * MI_IN_M","self._update(Decimal(value) * Decimal('1.0')/MI_IN_M)"],
    ["yard","yd","Decimal(self) * YD_IN_M","self._update(Decimal(value) * Decimal('1.0')/YD_IN_M)"],
    ["feet","ft","Decimal(self) * FT_IN_M","self._update(Decimal(value) * Decimal('1.0')/FT_IN_M)"],
    ["inch","inch","Decimal(self) * INCH_IN_M","self._update(Decimal(value) * Decimal('1.0')/INCH_IN_M)"],
    ["kilometers","km","Decimal(self) * KM_IN_M","self._update(Decimal(value) * Decimal('1.0')/KM_IN_M)"],
    ["centimeters","cm","Decimal(self) * CM_IN_M","self._update(Decimal(value) * Decimal('1.0')/CM_IN_M)"],
    ["millimeters","mm","Decimal(self) * MM_IN_M","self._update(Decimal(value) * Decimal('1.0')/MM_IN_M)"],
    ["nanometer","nm","Decimal(self) * NM_IN_M","self._update(Decimal(value) * Decimal('1.0')/NM_IN_M)"],
    ],
    [
    ["Area","sq_meters"],
    ["sq_meters","m2","Decimal(self)","self._update(Decimal(value))"],
    ["sq_miles","mi2","Decimal(self) * (MI_IN_M * MI_IN_M)","self._update(Decimal(value) * Decimal('1.0')/(MI_IN_M * MI_IN_M))"],
    ["sq_yard","yd2","Decimal(self) * (YD_IN_M * YD_IN_M)","self._update(Decimal(value) * Decimal('1.0')/(YD_IN_M * YD_IN_M))"],
    ["sq_feet","ft2","Decimal(self) * (FT_IN_M * FT_IN_M)","self._update(Decimal(value) * Decimal('1.0')/(FT_IN_M * FT_IN_M))"],
    ["sq_inch","inch2","Decimal(self) * (INCH_IN_M * INCH_IN_M)","self._update(Decimal(value) * Decimal('1.0')/(INCH_IN_M * INCH_IN_M))"],
    ["sq_kilometers","km2","Decimal(self) * (KM_IN_M * KM_IN_M)","self._update(Decimal(value) * Decimal('1.0')/(KM_IN_M * KM_IN_M))"],
    ["sq_centimeters","cm2","Decimal(self) * (CM_IN_M * CM_IN_M)","self._update(Decimal(value) * Decimal('1.0')/(CM_IN_M * CM_IN_M))"],
    ["sq_millimeters","mm2","Decimal(self) * (MM_IN_M * MM_IN_M)","self._update(Decimal(value) * Decimal('1.0')/(MM_IN_M * MM_IN_M))"],
    ],
    [
    ["Volumn","cubic_meters"],
    ["cubic_meters","m3","Decimal(self)","self._update(Decimal(value))"],
    ["cubic_miles","mi3","Decimal(self) * (MI_IN_M * MI_IN_M * MI_IN_M)","self._update(Decimal(value) * Decimal('1.0')/(MI_IN_M * MI_IN_M * MI_IN_M))"],
    ["cubic_yard","yd3","Decimal(self) * (YD_IN_M * YD_IN_M * YD_IN_M)","self._update(Decimal(value) * Decimal('1.0')/(YD_IN_M * YD_IN_M * YD_IN_M))"],
    ["cubic_feet","ft3","Decimal(self) * (FT_IN_M * FT_IN_M * FT_IN_M)","self._update(Decimal(value) * Decimal('1.0')/(FT_IN_M * FT_IN_M * FT_IN_M))"],
    ["cubic_inch","inch3","Decimal(self) * (INCH_IN_M * INCH_IN_M * INCH_IN_M)","self._update(Decimal(value) * Decimal('1.0')/(INCH_IN_M * INCH_IN_M * INCH_IN_M))"],
    ["cubic_kilometers","km3","Decimal(self) * (KM_IN_M * KM_IN_M * KM_IN_M)","self._update(Decimal(value) * Decimal('1.0')/(KM_IN_M * KM_IN_M * KM_IN_M))"],
    ["cubic_centimeters","cm3","Decimal(self) * (CM_IN_M * CM_IN_M * CM_IN_M)","self._update(Decimal(value) * Decimal('1.0')/(CM_IN_M * CM_IN_M * CM_IN_M))"],
    ["cubic_millimeters","mm3","Decimal(self) * (MM_IN_M * MM_IN_M * MM_IN_M)","self._update(Decimal(value) * Decimal('1.0')/(MM_IN_M * MM_IN_M * MM_IN_M))"],
    ],
    [
    ["Time","sec"],
    ["sec","sec","Decimal(self)","self._update(Decimal(value))"],
    ["min","min","Decimal(self) * Decimal('1.0')/SEC_IN_MIN","self._update(Decimal(value) * SEC_IN_MIN)"],
    ["hour","hr","Decimal(self) * Decimal('1.0')/(SEC_IN_MIN*MIN_IN_HR)","self._update(Decimal(value) * (SEC_IN_MIN*MIN_IN_HR))"],
    ["day","day","Decimal(self) * Decimal('1.0')/(HR_IN_DAY*SEC_IN_MIN*MIN_IN_HR)","self._update(Decimal(value) * (HR_IN_DAY*SEC_IN_MIN*MIN_IN_HR))"],
    ["week","wk","Decimal(self) * Decimal('1.0')/(DAY_IN_WK*HR_IN_DAY*SEC_IN_MIN*MIN_IN_HR)","self._update(Decimal(value) * (DAY_IN_WK*HR_IN_DAY*SEC_IN_MIN*MIN_IN_HR))"],
    ["year","yr","Decimal(self) * Decimal('1.0')/(DAY_IN_YR*HR_IN_DAY*SEC_IN_MIN*MIN_IN_HR)","self._update(Decimal(value) * (DAY_IN_YR*HR_IN_DAY*SEC_IN_MIN*MIN_IN_HR))"],
    ],
    [
    ["Velocity","meters_per_sec"],
    ["meters_per_sec","mps","Decimal(self)","self._update(Decimal(value))"],
    ["miles_per_sec","mips","Decimal(self) * MI_IN_M","self._update(Decimal(value) * Decimal('1.0')/MI_IN_M)"],
    ["miles_per_hr","mph","Decimal(self) * (MI_IN_M * SEC_IN_MIN * MIN_IN_HR)","self._update(Decimal(value) * Decimal('1.0')/(MI_IN_M * SEC_IN_MIN * MIN_IN_HR))"],
    ["ft_per_sec","fps","Decimal(self) * FT_IN_M","self._update(Decimal(value) * Decimal('1.0')/FT_IN_M)"],
    ["inch_per_sec","inchps","Decimal(self) * INCH_IN_M","self._update(Decimal(value) * Decimal('1.0')/INCH_IN_M)"],
    ["km_per_hour","kmph","Decimal(self) * (KM_IN_M * SEC_IN_MIN * MIN_IN_HR)","self._update(Decimal(value) * Decimal('1.0')/(KM_IN_M * SEC_IN_MIN * MIN_IN_HR))"],
    ["km_per_sec","kmps","Decimal(self) * KM_IN_M","self._update(Decimal(value) * Decimal('1.0')/KM_IN_M)"],
    ],
    [
    ["Acceleration","meters_per_sq_sec"],
    ["meters_per_sq_sec","mps2","Decimal(self)","self._update(Decimal(value))"],
    ["miles_per_sq_sec","mips2","Decimal(self) * MI_IN_M","self._update(Decimal(value) * Decimal('1.0')/MI_IN_M)"],
    ["miles_per_hr_per_sec","mphps","Decimal(self) * (MI_IN_M * SEC_IN_MIN * MIN_IN_HR)","self._update(Decimal(value) * Decimal('1.0')/(MI_IN_M * SEC_IN_MIN * MIN_IN_HR))"],
    ["ft_per_sq_sec","fps2","Decimal(self) * FT_IN_M","self._update(Decimal(value) * Decimal('1.0')/FT_IN_M)"],
    ["inch_per_sq_sec","ips2","Decimal(self) * INCH_IN_M","self._update(Decimal(value) * Decimal('1.0')/INCH_IN_M)"],
    ["km_per_hour_per_sec","kmphps","Decimal(self) * (KM_IN_M * SEC_IN_MIN * MIN_IN_HR)","self._update(Decimal(value) * Decimal('1.0')/(KM_IN_M * SEC_IN_MIN * MIN_IN_HR))"],
    ["km_per_sq_sec","kmps2","Decimal(self) * KM_IN_M","self._update(Decimal(value) * Decimal('1.0')/KM_IN_M)"],
    ],
    [
    ["Mass","kilogram"],
    ["kilogram","kg","Decimal(self)","self._update(Decimal(value))"],
    ["gram","g","Decimal(self) * Decimal('1000.0')","self._update(Decimal(value) / Decimal('1000.0'))"],
    ["ounce","oz","Decimal(self) * OZ_IN_G * Decimal('1000.0')","self._update(Decimal(value) / OZ_IN_G / Decimal('1000.0'))"],
    ["pounds","lbm","Decimal(self) * (OZ_IN_G / OZ_IN_LB) * Decimal('1000.0')","self._update(Decimal(value)* OZ_IN_LB / OZ_IN_G / Decimal('1000.0') )"],
    ],
    [
    ["Force","newton"], # m*kg*s**2
    ["newton","N","Decimal(self)","self._update(Decimal(value))"],
    ["kilogram-force","kgf","Decimal(self) / GRAVITY","self._update(Decimal(value) * GRAVITY)"],
    ["dyne","dyn","Decimal(self) * Decimal('100000.0')","self._update(Decimal(value) / Decimal('100000.0'))"],
    ["pound-force","lbf","Decimal(self) * (G_IN_KG * OZ_IN_G) / (OZ_IN_LB*GRAVITY)","self._update(Decimal(value) * (OZ_IN_LB * GRAVITY) / (G_IN_KG * OZ_IN_G))"],
    ], 
    [
    ["Weight","kilogram"], # m*kg*s**2
    ["kilogram","kg","Decimal(self)","self._update(Decimal(value))"],
    ["gram","g","Decimal(self) * G_IN_KG ","self._update(Decimal(value) / G_IN_KG)"],
    ["ounce","oz","Decimal(self) * G_IN_KG * OZ_IN_G ","self._update(Decimal(value) / (G_IN_KG * OZ_IN_G))"],
    ["pounds","lbm","Decimal(self) * (G_IN_KG * OZ_IN_G) / (OZ_IN_LB)","self._update(Decimal(value) * (OZ_IN_LB ) / (G_IN_KG * OZ_IN_G))"],
    ], 
    [
    ["Pressure","pascal "],
    ["pascal","Pa","Decimal(self)","self._update(Decimal(value))"],
    ["newton_per_sq_m","Nm2","Decimal(self)","self._update(Decimal(value))"],
    ["kilogram_per_sq_m","kgfpm2","Decimal(self) * Decimal('1.0')/GRAVITY","self._update(Decimal(value) * GRAVITY)"],
    ["pound_per_sq_inch","psi","Decimal(self) * (LB_IN_NEWTON/(INCH_IN_M * INCH_IN_M))","self._update(Decimal(value) * (INCH_IN_M * INCH_IN_M) / LB_IN_NEWTON)"],
    ["pound_per_sq_ft","psf","Decimal(self) * LB_IN_NEWTON/(FT_IN_M * FT_IN_M)","self._update(Decimal(value) * (FT_IN_M * FT_IN_M) / LB_IN_NEWTON)"],
    ],
    [
    ["Frequency","Frequency"],
    ["hertz","Hz","Decimal(self)","self._update(Decimal(value))"],
    ["KHz","KHz","Decimal(self) * Decimal('1.0')/Decimal(1.0e3)","self._update(Decimal(value) * Decimal('1.0e3'))"],
    ["MHz","MHz","Decimal(self) * Decimal('1.0')/Decimal(1.0e6)","self._update(Decimal(value) * Decimal('1.0e6'))"],
    ["GHz","GHz","Decimal(self) * Decimal('1.0')/Decimal(1.0e9)","self._update(Decimal(value) * Decimal('1.0e9'))"],
    ],
    [
    ["Power","Power"],
    ["watts","W","Decimal(self)","self._update(Decimal(value))"],
    ["kilowatt","KW","Decimal(self) * Decimal('1.0')/Decimal('1.0e3')","self._update(Decimal(value) * Decimal('1.0e3'))"],
    ["megawatt","MW","Decimal(self) * Decimal('1.0')/Decimal('1.0e6')","self._update(Decimal(value) * Decimal('1.0e6'))"],
    ["Horsepower","hp","Decimal(self) * Decimal('1.0')/W_IN_HP","self._update(Decimal(value) * W_IN_HP)"],
    ["joulepersec","jps","Decimal(self)","self._update(Decimal(value))"],
    ],
    [
    ["Temperature","degreeK"],
    ["Kelvin","K","Decimal(self)","self._update(Decimal(value))"],
    ["Fahrenheit","F","((Decimal(self) - Decimal('273.15')) * Decimal('9.0')/Decimal('5.0')) + Decimal('32.0')","self._update((Decimal(value) - Decimal('32.0')) * (Decimal('5.0')/Decimal('9.0')) + Decimal('273.15'))"],
    ["Celsius","C","Decimal(self) - Decimal('273.15')","self._update(Decimal(value) + Decimal('273.15'))"],
    ],
]

def build_class(table):
    "build a class for each table i.e. Distance,Velocity,etc."
    name, baseunits = table[0]
    s = '\nclass %(name)s(Decimal):\n' % locals()
    s += '    __slots__ = ("_update",) # generate AttributeError on illegal property; example: if d.yds instead of d.ydgenerate AttributeError example: if d.yds not d.yd\n'
    return s

def build_init(table):
    "update method"
    s = """
    def _update(self,dec):
        self._exp  = dec._exp
        self._sign = dec._sign
        self._int  = dec._int
        self._is_special  = dec._is_special
"""
    return s

def build_str_funct(table):
    "str method"
    fmt1 = "    def __str__(self):\n        s = ''\n"
    fmt2 = "        s += '%%g %(units)s (%(abrev)s)\\n' %% self.%(abrev)s\n"
    name, baseunits = table[0]
    s = fmt1 % locals()
    for data in table[1:]:
        if len(data) == 3:
            units, abrev, value = data
        else:
            units, abrev, value, value2 = data
        s += fmt2 % locals()
    s += '        return s[:-1]\n'
    return s

def build_repr_funct(table):
    "repr method"
    fmt1 = "    def __repr__(self):\n        s = ''\n"
    fmt2 = "        s += '%%r %(units)s (%(abrev)s)\\n' %% self.%(abrev)s\n"
    name, baseunits = table[0]
    s = fmt1 % locals()
    for data in table[1:]:
        if len(data) == 3:
            units, abrev, value = data
        else:
            units, abrev, value, value2 = data
        s += fmt2 % locals()
    s += '        return s[:-1]\n'
    return s


def build_methods(table):
    "setter and getter property methods"
    fmt = """    @property
    def %(abrev)s(self):
        return eval("%(value)s")
    @%(abrev)s.setter
    def %(abrev)s(self, value):
        eval("%(value2)s")\n"""

    s = ''
    name, baseunits = table[0]
    for data in table[1:]:
        if len(data) == 3:
            units, abrev, value = data
            value2 = str(Decimal(1.0)/eval(value))
        else:
            units, abrev, value, value2 = data
        s += fmt % locals()
    return s

def build_header(header,tables,examples):
    "build module description"
    s = header
    s += 'Conversions:\n'
    for table in tables:
        s += '    %s\n' % table[0][0]
    s += examples
    s += '\n"""\n'
    return s


def build_doctest_call(modulename, testfilename):
    "create method to call doctest on module and module test file"
    s = """
def test():
    "test method tests examples and testfile"
    print '\\n**** %s test ****\\n'
    import doctest
    import %s

    doctest.testmod(%s, verbose=True, report=True)
    print doctest.master.summarize()

    doctest.testfile('%s', verbose=True, report=True)
    print doctest.master.summarize()
    
if __name__ == '__main__':
    test()
""" % (modulename,modulename,modulename,testfilename)
    return s

def build_module(tables, modulename):
    "build module from data table "
    s = '"""\n'
    s += build_header(header, tables, examples)

    s += constants
    for table in tables:
        s += build_class(table)
        s += build_init(table)
        s += build_str_funct(table)
        s += build_repr_funct(table)
        s += build_methods(table)
    s += build_doctest_call(modulename, testfilename)
    return s

def build_test(table):
    "build a test for all getters and setters for each class"
    name, baseunits = table[0]
    s = '\n%s conversion class\n' % name
    s += '>>> from conversion import %s\n' % (name)
    s += '>>> %s = %s(0.0)\n' % (name.lower()[0],name)
    args = [arg[1] for arg in table[1:]]
    for arg in args:
        s += '>>> %s.%s = 1.0\n' % (name.lower()[0],arg)
        s += '>>> print %s\n' % (name.lower()[0])
        x = eval('%s()' % name)
        exec('x.%s = 1.0' % arg)
        for line in str(x).split('\n'):
            s += '%s\n' % line
        s += '>>> %s\n' % (name.lower()[0])
        x = eval('%s()' % name)
        exec('x.%s = 1.0' % arg)
        for line in repr(x).split('\n'):
            s += '%s\n' % line
    s += '\n'
    return s


def build_doctest(modulename,testfilename):
    "builds test file for testing %s.py based on table data" % (modulename)
    s = 'building %s' % testfilename
    s += '\n## **** %s Test  ****\n' % (modulename)
    s += 'from %s import *' % (modulename)
    s += '"""'
    for table in tables:
        s += build_test(table)
    return s

if __name__ == '__main__':
    filename = 'conversion.py'
    modulename = filename[:-3]
    testfilename = modulename+'Test.txt'
    
    print 'building', filename
    fp = open(filename,'w')
    s = build_module(tables, modulename)
    print >>fp,s
    fp.close()

    from conversion import *
    print 'building', testfilename
    fp = open(testfilename,'w')
    s = build_doctest(modulename,testfilename)
    print >>fp,s
    fp.close()
