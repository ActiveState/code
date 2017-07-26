#!/usr/local/bin/python
# -*- coding: ISO-8859-1 -*-

import sys
import os
sys.path = [os.getcwd()] + sys.path
import sitecustomize
reload(sitecustomize)
