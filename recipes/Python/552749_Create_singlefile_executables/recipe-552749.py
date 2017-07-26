@echo off
rem = """

py25 -x "%~f0" 
goto endofPython """

from distutils.core import setup
import py2exe
import shutil
import sys, os

sys.argv += ['py2exe', '-b1', '-d./']

setup(
    # use "console = " for console-based apps
    windows=["cron.py"],
    zipfile=None
    )

shutil.rmtree('build')
os.remove('w9xpopen.exe')
rem = """
:endofPython """
