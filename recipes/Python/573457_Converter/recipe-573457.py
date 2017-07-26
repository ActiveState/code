#On the name of ALLAH
#Author : Fouad Teniou
#Date : 17/06/08
#version :2.4
import re       #Get re class
import math     #Get math class
class Converter:
    def __init__(self, other,unit=0):
        self.unit = unit
        self.other = other
    def __mul__(self):
        return self.unit * self.other
    def __div__(self):
       return round((self.other/self.unit),2)
    def __repr__(self):
        return "\n <Converter : Operation of %s, to convert the value of (%s)>" % (self.__class__.__name__,(self.other)) #class name and the value 

class FeetMetre(Converter):
    def __init__(self,other):
        Converter.__init__(self,other,0.3048) #Run Converter init
    def measure(self):
        print '\n\t\t\t',"Feet --> Metre"
        m = re.match(r"(?P<int>\d+)\.(\d*)", str("%2.2f" % self.other))
        L = round(((int(m.group(1)))*(self.unit))+(((float(m.group(2))/12))*(self.unit)),3)
        M = re.match(r"(?P<int>\d+)\.(\d*)", str(L))
        print '\n\t\t\t',m.group(1)+"ft",m.group(2)+"in" +" = "+ M.group(1)+"m",M.group(2)[:2]+"cm"
        
class MetreFeet(FeetMetre):
    def __init__(self,other):
        FeetMetre.__init__(self,other)      #Run FeetMetre init
    def measure(self):
        print '\n\t\t\t',"Metre --> Feet"
        n = re.match(r"(?P<int>\d+)\.(\d*)", str("%2.2f" % self.other))
        o = re.match(r"(?P<int>\d+)\.(\d*)", str(Converter.__div__(self)))
        print '\n\t\t\t',n.group(1)+"m",n.group(2)+"cm" +" = "+ o.group(1)+"ft","%2.2s" % (str(round((float(o.group(2))*(0.12)),0)))+"in"

class MileKilometre(Converter):
    def __init__(self,other):
        Converter.__init__(self,other,1.609) #Run Converter init
    def measure(self):
        print '\n\t\t\t',"Mile --> KiloMetre"
        print '\n\t\t\t',str(self.other)+'ml'+' = '+"%2.2f" % float(Converter.__mul__(self))+'Km'
        
class KilometreMile(MileKilometre):
    def __init__(self,other):
        MileKilometre.__init__(self,other) #Run MileKilometre init
    def measure(self):
        print '\n\t\t\t',"Kilometre --> Mile"
        print '\n\t\t\t',(str(self.other))+'Km'+' = '+ str(Converter.__div__(self))+'ml'
        
class YardMetre(Converter):
    def __init__(self,other):
        Converter.__init__(self,other,0.9144)  #Run Converter init
    def measure(self):
        print '\n\t\t\t',"Yard --> Metre"
        m = re.match(r"(?P<int>\d+)\.(\d*)", str("%2.2f" % (Converter.__mul__(self))))
        print '\n\t\t\t',str(self.other)+'yd'+' = '+ m.group(1)+'m' ,"%2.2s" % (m.group(2))+'cm'
        
class MetreYard(YardMetre):
    def __init__(self,other):
        YardMetre.__init__(self,other)          #Run YardMetre init
    def measure(self):
        print '\n\t\t\t',"Metre --> Yard"
        m = re.match(r"(?P<int>\d+)\.(\d*)", str("%2.2f" % self.other))
        print '\n\t\t\t',m.group(1)+'m',m.group(2)+'cm'+' = '+ str(Converter.__div__(self))+'yd'

class PoundKilo(Converter):
    def __init__(self,other):
        Converter.__init__(self,other,0.4536)  #Run Converter init
    def measure(self):
        print '\n\t\t\t',"Pound  --> Kilogram"
        m = re.match(r"(?P<int>\d+)\.(\d*)", str("%2.2f" % self.other))
        L = "%2.3f" % (round(((int(m.group(1)))*(self.unit))+(((float(m.group(2))/16))*(self.unit)),3))
        M = re.match(r"(?P<int>\d+)\.(\d*)", str(  L))
        print '\n\t\t\t',m.group(1)+"lb",m.group(2)+"oz" +" = "+ M.group(1)+"Kg",M.group(2)+"g"
        
class KiloPound(PoundKilo):
    def __init__(self,other):
        PoundKilo.__init__(self,other)          #Run PoundKilo init
    def measure(self):
        print '\n\t\t\t',"Kilogram  --> Pound"
        n = re.match(r"(?P<int>\d+)\.(\d*)", str("%2.3f" % self.other))
        o = re.match(r"(?P<int>\d+)\.(\d*)", str(Converter.__div__(self)))
        print '\n\t\t\t',n.group(1)+"Kg",n.group(2)+"g" +" = "+ o.group(1)+"lb","%2.2s" % (str(round((float(o.group(2))*(0.16)),0)))+"oz"

class GallonLitre(Converter):
    def __init__(self,other):
        Converter.__init__(self,other,4.55)     #Run Converter init
    def measure(self):
        print '\n\t\t\t',"British and American Gallon --> Litre"
        p=  re.match(r"(?P<int>\d+)\.(\d*)", str ( float(Converter.__mul__(self))))
        print '\n\t\t\t',str(self.other)+'(BR)gal'+' = '+ ("%2.2f" % float(self.other*1.2))+'(AM)gal'+' = '+p.group(1)+'l' ,"%2.2s" % (p.group(2))+'cl'
        
class LitreGallon(GallonLitre):
    def __init__(self,other):
        GallonLitre.__init__(self,other)        #Run GallonLitre init
    def measure(self):
        print '\n\t\t\t',"Litre --> British and American Gallon"
        q = re.match(r"(?P<int>\d+)\.(\d*)", str("%2.2f" % self.other))
        print '\n\t\t\t',q.group(1)+"l",q.group(2)+"cl" +" = " ,"%2.2f" % float(Converter.__div__(self))+'(BR)gal'+' = '"%2.2f" % float((Converter.__div__(self))*1.2)+'(AM)gal'

class TemperatureD(Converter):
    def __init__(self,other):
        Converter.__init__(self,other,1.8)       #Run Converter init
    def measure(self):
        print '\n\t\t\t',"Degree Celsius --> Fahrenheit"
        print '\n\t\t\t',str(self.other)+chr(248)+'C'+' = '+str( "%2.1f" % (32 + float(Converter.__mul__(self))))+chr(248)+'F'
        
class TemperatureF(TemperatureD):
    def __init__(self,other):
        TemperatureD.__init__(self,other)       #Run TemperatureD init
    def measure(self):
        print '\n\t\t\t',"Fahrenheit --> Degree Celsius"
        B = self.other-32
        self.other = B
        print '\n\t\t\t',str(self.other+32)+chr(248)+'F'+' = '+str( "%2.1f" %  ( float(Converter.__div__(self))))+chr(248)+'C' 
        

if __name__ == "__main__":
    a=MetreFeet(2.0)
    print a
    a.measure()
    b=FeetMetre(6.07)
    print b
    b.measure()
    c = MileKilometre(1)
    print c
    c.measure()
    d = KilometreMile(1)
    print d
    d.measure()
    e = YardMetre(3)
    print e
    e.measure()
    f = MetreYard(3.8)
    print f
    f.measure()
    g = PoundKilo(12.14)
    print g
    g.measure()
    h = KiloPound(5.890)
    print h
    h.measure()
    k = GallonLitre(2.22)
    print k
    k.measure()
    l = LitreGallon(5)
    print l
    l.measure()
    m = TemperatureD(-10)
    print m
    m.measure()
    n = TemperatureF(14)
    print n
    n.measure()
    
  ###############################################################
  
   
    
    
#c:\Python26>python "C:\Fouad Teniou\Documents\Programs\Converter5.py"

# <Converter : Operation of MetreFeet, to convert the value of (2.0)>

#                        Metre --> Feet

#                        2m 00cm = 6ft 7.in

# <Converter : Operation of FeetMetre, to convert the value of (6.07)>

#                        Feet --> Metre

#                        6ft 07in = 2m 00cm

# <Converter : Operation of MileKilometre, to convert the value of (1)>

#                        Mile --> KiloMetre

#                        1ml = 1.61Km

# <Converter : Operation of KilometreMile, to convert the value of (1)>

#                        Kilometre --> Mile

#                        1Km = 0.62ml

# <Converter : Operation of YardMetre, to convert the value of (3)>

#                        Yard --> Metre

#                        3yd = 2m 74cm

# <Converter : Operation of MetreYard, to convert the value of (3.8)>

#                        Metre --> Yard

#                        3m 80cm = 4.16yd

# <Converter : Operation of PoundKilo, to convert the value of (12.14)>

#                        Pound  --> Kilogram

#                        12lb 14oz = 5Kg 840g

# <Converter : Operation of KiloPound, to convert the value of (5.89)>

#                        Kilogram  --> Pound

#                        5Kg 890g = 12lb 16oz

# <Converter : Operation of GallonLitre, to convert the value of (2.22)>

#                        British and American Gallon --> Litre

#                        2.22(BR)gal = 2.66(AM)gal = 10l 10cl

# <Converter : Operation of LitreGallon, to convert the value of (5)>

#                        Litre --> British and American Gallon

#                        5l 00cl =  1.10(BR)gal = 1.32(AM)gal

# <Converter : Operation of TemperatureD, to convert the value of (-10)>

#                        Degree Celsius --> Fahrenheit

#                        -10°C = 14.0°F

# <Converter : Operation of TemperatureF, to convert the value of (14)>

#                        Fahrenheit --> Degree Celsius

#                        14°F = -10.0°C
