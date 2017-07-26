My original PATHEXT variable. 

M:\>echo %PATHEXT%
.COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH

Using Control Panel -> System -> Advanced -> Environment Variables, I edited this and added .PY.

M:\>echo %PATHEXT%
.COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.PY

I have M:\bin in my PATH as well, so now DOS just finds the commands.

M:\>type bin\pytest.py

import sys

print "Hello from MS Windows:", sys.getwindowsversion()

M:\>pytest
Hello from MS Windows: (5, 1, 2600, 2, 'Service Pack 2')
