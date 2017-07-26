'''
Simple script to allow us to run paster more easily (but probably in an unintended way)
'''
import subprocess
import argparse
import os
import sys
import signal

#change this to be whatever your project will be called, 
import my_paster_package

def main():
    parser = argparse.ArgumentParser(description='Run as --dev or --prod.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--dev', action="store_true", default=False)
    group.add_argument('--prod', action="store_true", default=False)
    
    args = parser.parse_args()
    
    #make sure we are running the paster out of the venv by finding the bin directory that this script is being
    #run out of
    bin_dir = os.path.dirname(sys.executable)
    config_file_dir = my_paster_package.__path__[0]
    
    if args.dev:
        p = subprocess.Popen("./paster serve %s/development.ini --reload" % (config_file_dir + "/.."), 
                             shell=True, cwd=bin_dir)
        
        
    elif args.prod:
        paster_pid_file = bin_dir+"/paster.pid"
        
        p = subprocess.Popen("./paster serve %s/production.ini --pid-file=%s" % (config_file_dir, paster_pid_file), 
                             shell=True, cwd=bin_dir)
        
        #attach a signal handler so we can kill off the subprocesses when supervisor kills this script
        #otherwise the kill signal doens't propegate to all the paster processes
        def signal_handler(signal, frame):
            if os.path.exists(paster_pid_file):
                paster_pid = open(paster_pid_file, "r").read()
                os.system("kill -2 %s" % (paster_pid))
            else:
                print "Warning: Could not find paster pid file, paster might not have properly terminated"
                
        signal.signal(signal.SIGTERM, signal_handler)

    else:
        raise Exception("Please choose either --dev or --prod")
    
    sts = os.waitpid(p.pid, 0)[1]
    
    #return the code in case of a problem
    sys.exit(sts)

if __name__ == '__main__':
    main()
