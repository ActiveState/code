@echo off
rem = """
Do any custom setup like setting environment variables etc if required here ...

python -x "%~f0" %1 %2 %3 %4 %5 %6 %7 %8 %9
goto endofPython """

# Your python code goes here ..
   
if __name__ == "__main__":
	print "Hello World"

rem = """
:endofPython """
