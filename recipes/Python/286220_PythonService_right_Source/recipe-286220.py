"""
From "Python Programming on Win32 Chapter 18 - Windows NT Services".

The Event Log facilities of servicemanager use the name of the executable as the application name. 
This means that by default, the application name will be PythonService. 
The only way this can be changed is to take a copy of PythonService.exe 
and rename it to something of your liking (it's only around 20 KB!). 
Alternatively, you may wish to use the Event Log natively, as described later in this chapter.

"""

# Here is another way of changing the source name:

class PyMyService(win32serviceutil.ServiceFramework):
    _svc_name_ = "PyMyService"
    _svc_display_name_ = "Python Service With The Right Name"
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)

    def SvcDoRun(self):
        import servicemanager
        # Add these two lines and the source will be "PyMyService"
        win32evtlogutil.AddSourceToRegistry(self._svc_name_, servicemanager.__file__)
        servicemanager.Initialize(self._svc_name_, servicemanager.__file__)
        #
        servicemanager.LogMsg(
               servicemanager.EVENTLOG_INFORMATION_TYPE,
               servicemanager.PYS_SERVICE_STARTED,
               (self._svc_name_, ""))
	               
        servicemanager.LogInfoMsg("Info")  # Event is 255
        servicemanager.LogErrorMsg("Error")  # Event is 255
        servicemanager.LogWarningMsg("Warn")  # Event is 255
        # or
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
               0xF000, ("Info",))   	# Event is 61440
        servicemanager.LogMsg(servicemanager.EVENTLOG_ERROR_TYPE, 
               0xF001, ("Error",))   	# Event is 61441
        servicemanager.LogMsg(servicemanager.EVENTLOG_WARNING_TYPE, 
               0xF002, ("Warn",))   	# Event is 61442

	# events up to 0xF008 are avaliable
