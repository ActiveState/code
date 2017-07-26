from new import classobj

def connectClasses( newClassName, parentClass, childClass ):
	# Create an empty shell class with the passed in parentClass
	# as the parent.
	DupedChildClass =  classobj( newClassName, (parentClass,), {} )

	# Inject the parent class in to the child as a member, in case
	# the child wants to call the parent.
	DupedChildClass._parentClass = parentClass
	
	# Copy references to all the members of the child class passed in
	# to the new version of the child class connected to the 
	# given parent class.  i.e. fill in the dupedChildClass shell created
	# on previous line.	
	for k,v in childClass.__dict__.items():
		# U can't overwrite the doc string for some reason
		if k != '__doc__':
			setattr( DupedChildClass, k, v )
			
	return DupedChildClass

    
class Person:
      def sayHello( self ):
            print "Hi, I am a %s."  % self._getMyGender()
            
class Man( Person ):    
      def _getMyGender( self ):
            return "man"
        
class Woman( Person ): 
      def _getMyGender( self ):
            return "woman"    
 
class Insecure:
      def _getMyGender( self ):
            return self._parentClass._getMyGender( self ) + ', if that is OK' 

# Create the two new classes
InsecureMan = connectClasses( 'InsecureMan', Man, Insecure )
InsecureWoman = connectClasses( 'InsecureWoman', Woman, Insecure )

# Instantiate classes
iMan = InsecureMan()
iWoman = InsecureWoman()
man = Man()
woman = Woman()

# Test the classes
man.sayHello()
woman.sayHello()
iMan.sayHello()
iWoman.sayHello()


# Expected output
'''
Hi, I am a man.
Hi, I am a woman.
Hi, I am a man, if that is OK.
Hi, I am a woman, if that is OK.
'''
