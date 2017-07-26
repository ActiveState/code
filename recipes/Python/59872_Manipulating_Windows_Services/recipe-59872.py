import win32serviceutil

def service_info(action, machine, service):
    if action == 'stop': 
        win32serviceutil.StopService(service, machine)
        print '%s stopped successfully' % service
    elif action == 'start': 
        win32serviceutil.StartService(service, machine)
        print '%s started successfully' % service
    elif action == 'restart': 
        win32serviceutil.RestartService(service, machine)
        print '%s restarted successfully' % service
    elif action == 'status':
        if win32serviceutil.QueryServiceStatus(service, machine)[1] == 4:
            print "%s is running normally" % service 
        else:
            print "%s is *not* running" % service 

if __name__ == '__main__':
    machine = 'cr582427-a'
    service = 'Zope23'
    action = 'start'
    service_info(action, machine, service)
