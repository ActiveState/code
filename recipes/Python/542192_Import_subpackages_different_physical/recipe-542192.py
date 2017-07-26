"""
Example directory structure:

/test_company_in.py
/folder1/
  /company_inc/
    __init__.py  <- Apply code here!
    /toola/
      __init__.py
      ...
/folder2/
  /company_inc/
    __init__.py  <- Apply code here!
    /toolb/
      __init__.py
      ...
"""

# /folder1/company_inc/toola/__init__.py
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

# /folder2/company_inc/toolb/__init__.py
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

#/test_company_in.py
import sys
sys.path += ["folder1", "folder2"]
import company_inc.toola
import company_inc.toolb
