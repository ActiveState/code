#!/usr/bin/env python
# -*- coding: utf-8 -*
    
"""
1. Install Python 2.3 from python.org to your computer.
2. Install your favourite modules:
    Recommended:
        pywin32 module - accessing COM and other lovely windows stuff
        subprocess module - launching subprocesses from ya login scripts
        ctypes module - wrap any win32api        
3. Copy your Python23 folder to the NETLOGON (or any shared network) directory.
4. Copy these dll files from your system directory to that folder
    python23.dll
    pythoncom23.dll - pywin32
    pywintypes23.dll - pywin32
5. Running your python scripts
    create a batch file with the lines:
        rem - path to python23 folder, %\0.. refers to the current directory
        SET PYTHONPATH=%0\..\Python23
        rem - path to script to execute
        %PYTHONPATH%\python.exe %0\..\login.py
6. What can you do in python? Endless, see below...
"""

# pywintypes must be imported b4 any win32 modules
import pywintypes
import win32com.client

# Disconnect previously mapped drives.
wshnetwork = win32com.client.Dispatch('Wscript.Network')
network_drives = wshnetwork.EnumNetworkDrives()
for mapped_drive in [network_drives.Item(i) 
                     for i in range(0, network_drives.Count() -1 , 2) 
                     if network_drives.Item(i)]:
    wshnetwork.RemoveNetworkDrive(mapped_drive, True, True)

# Network drive mapping.
drive_mappings = [
    ('I:', '\\\\server1\\users'),
    ('J:', '\\\\server2\\sharing')]
for drive_letter, network_path in drive_mapping:
    try:
        wshnetwork.MapNetworkDrive(drive_letter, network_path)
    except Exception, err:
        print err

# Batch execute other python files in some_dir.
import sys
sys.path.append("some_dir")
# virusupdate.py
import virusupdate
# checkhotfix.py
import checkhotfix

# Other advantages:
# GUI for your logon scripts with TKInter, Win32Gui.
# Centrally managed python installation.
# Access to the Win32 API.
# Robust error handling.
# Not to mention, multithreading!
# Can also be used with Group Policy scripts.
