###################################################################################################################

    import os
    import sys


    class Daemonize:
        """ Generic class for creating a daemon"""

        def daemonize(self):
            try:
                #this process would create a parent and a child
                pid = os.fork()
                if pid > 0:
                    # take care of the first parent
                    sys.exit(0)
            except OSError, err:
                sys.stderr.write("Fork 1 has failed --> %d--[%s]\n" % (err.errno,
                                                                  err.strerror))
                sys.exit(1)

            #change to root
            os.chdir('/')
            #detach from terminal
            os.setsid()
            # file to be created ?
            os.umask(0)

            try:
                # this process creates a parent and a child
                pid = os.fork()
                if pid > 0:
                    print "Daemon process pid %d" % pid
                    #bam
                    sys.exit(0)
            except OSError, err:
                sys.stderr.write("Fork 2 has failed --> %d--[%s]\n" % (err.errno,
                                                                  err.strerror))
                sys.exit(1)

            sys.stdout.flush()
            sys.stderr.flush()

        def start_daemon(self):
            self.daemonize()
            self.run_daemon()

        def run_daemon(self):
        """override"""
            pass

###################################################################################################################

    from Daemonize import Daemonize
    from email.MIMEText import MIMEText
    import os
    import smtplib
    from smtplib import SMTPException
    import time


     class WatchFile(Daemonize):

        def __init__(self, file_path, size_limit=15728640):
            self.file = os.path.realpath(file_path)
            print '---'
            assert os.path.isfile(self.file), '%s does not exist' % self.file
            print '+++'
            self.userhome = os.getenv('HOME')
            self.smtpserver = '*your-host*'
            self.recipient_list = ['recipient@domain']
            self.sender = 'sender@domain'
            self.file_size_limit = size_limit
            self.email_body = os.path.join(self.userhome, 'email-msg.txt')
            self.interval = 3600
            self.log_file = os.path.join(self.userhome, 'inboxlog.txt')

        def send_an_email(self):
           """Method to send email to the recipients"""
           email_body = open(self.email_body, 'r').read()
           msg = MIMEText(email_body)
           msg['Subject'] = 'Your email inbox has exceeded size !'
           msg['From'] = 'Inbox WatchDog'
           msg['Reply-to'] = None
           msg['To'] = self.recipient_list

           session_obj = smtplib.SMTP()
           session_obj.connect(self.smtpserver)
           try:
               session_obj.sendmail(self.sender, self.recipient_list, msg.as_string())
           except SMTPException:
                print "Unable to send emails."
           finally:
               session_obj.close()

        def watch(self):
            """Method to watch your inbox. This also logs the time when your 
               inbox was last checked."""
            current_file_size = os.path.getsize(self.file)
            if current_file_size > self.file_size_limit:
                self.send_an_email()
            f = open(self.log_file, 'a')
            f.write('Last checked on : %s' % time.asctime(time.localtime(time.time())))
            f.write('\n')
            f.close()

        def run_daemon(self):
            """Over ridden method from Daemonize.This starts the daemon."""
            while 1:
                self.watch()
                time.sleep(self.interval)


    if __name__ == '__main__':
        watchdog = WatchFile('path-to-your-inbox')
        watchdog.start_daemon()
