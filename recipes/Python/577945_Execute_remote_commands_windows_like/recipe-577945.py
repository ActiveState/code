#! /usr/bin/python

__author__="ofer.helman"
__date__ ="$Nov 9, 2011 9:30:26 PM$"

import os
import wmi
import shutil
import win32wnet


REMOTE_PATH = 'c:\\'

def main():
    ip = 'or_hostname'
    username = 'user'
    password = 'pass'
    server = WindowsMachine(ip, username, password)
    print server.run_remote('ipconfig', async=False, output=True)

def create_file(filename, file_text):
    f = open(filename, "w")
    f.write(file_text)
    f.close() 

class WindowsMachine:
    def __init__(self, ip, username, password, remote_path=REMOTE_PATH):
        self.ip = ip
        self.username = username
        self.password = password
        self.remote_path = remote_path
        try:
            print "Establishing connection to %s" %self.ip
            self.connection = wmi.WMI(self.ip, user=self.username, password=self.password)
            print "Connection established"
        except wmi.x_wmi:
            print "Could not connect to machine"
            raise

    def run_remote(self, cmd, async=False, minimized=True, output=False):
        """
        this function runs cmd on remote machine, using wmi. the function create a .bat file,
        copies it to the remote machine, and runs the .bat file
        inputs: cmd - command to run
                async - False, waits for command to finish, True, return immidiatly
                mimimized - window state
                output - True, returns the command's output
        output: return value of the command
                output of the command if true
        """
        output_data = None
        pwd = os.getcwd()
        bat_local_path = os.path.join(pwd, 'output.bat')
        bat_remote_path = os.path.join(self.remote_path, 'output.bat')
        output_remote_path = os.path.join(self.remote_path, 'output.out')
        output_local_path = os.path.join(pwd, 'output.out')
        text = cmd + " > " + output_remote_path
        create_file(bat_local_path, text)
        self.net_copy(bat_local_path, self.remote_path)
        batcmd = bat_remote_path

        SW_SHOWMINIMIZED = 0
        if not minimized:
            SW_SHOWMINIMIZED = 1
        print "Executing %s" %cmd
        startup = self.connection.Win32_ProcessStartup.new (ShowWindow=SW_SHOWMINIMIZED)
        process_id, return_value = self.connection.Win32_Process.Create (CommandLine=batcmd, ProcessStartupInformation=startup)
        if async:
            watcher = self.connection.watch_for (
                                  notification_type="Deletion",
                                  wmi_class="Win32_Process",
                                  delay_secs=1,
                                  )
            watcher ()

        if output and not async:
            print 'copying back ' + output_remote_path
            self.net_copy_back(output_remote_path, output_local_path)
            output_data = open(output_local_path, 'r')
            output_data = "".join(output_data.readlines())
            self.net_delete(output_remote_path)
        self.net_delete(bat_remote_path)
        return return_value, output_data

    def net_copy(self, source, dest_dir, move=False):
        """ Copies files or directories to a remote computer. """
        print "Start copying files to " + self.ip
        if self.username == '':
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            else:
                # Create a directory anyway if file exists so as to raise an error.
                 if not os.path.isdir(dest_dir):
                     os.makedirs(dest_dir)
            shutil.copy(source, dest_dir)

        else:
            self._wnet_connect()

            dest_dir = self._covert_unc(dest_dir)

            # Pad a backslash to the destination directory if not provided.
            if not dest_dir[len(dest_dir) - 1] == '\\':
                dest_dir = ''.join([dest_dir, '\\'])

            # Create the destination dir if its not there.
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            else:
                # Create a directory anyway if file exists so as to raise an error.
                 if not os.path.isdir(dest_dir):
                     os.makedirs(dest_dir)

            if move:
                shutil.move(source, dest_dir)
            else:
                shutil.copy(source, dest_dir)

    def net_copy_back(self, source_file, dest_file):
        """ Copies files or directories to a remote computer. """
        print "Start copying files " + source_file +  " back from " + self.ip
        if self.username == '':
            shutil.copy(source_file, dest_file)
        else:
            self._wnet_connect()
            source_unc =  self._covert_unc(source_file)
            shutil.copyfile(source_unc, dest_file)

    def _wnet_connect(self):
        unc = ''.join(['\\\\', self.ip])
        try:
            win32wnet.WNetAddConnection2(0, None, unc, None, self.username, self.password)
        except Exception, err:
            if isinstance(err, win32wnet.error):
                # Disconnect previous connections if detected, and reconnect.
                if err[0] == 1219:
                    win32wnet.WNetCancelConnection2(unc, 0, 0)
                    return self._wnet_connect(self)
            raise err

    def _covert_unc(self, path):
        """ Convert a file path on a host to a UNC path."""
        return ''.join(['\\\\', self.ip, '\\', path.replace(':', '$')])

    def copy_folder(self, local_source_folder, remote_dest_folder):
        files_to_copy = os.listdir(local_source_folder)
        for file in files_to_copy:
            file_path = os.path.join(local_source_folder, file)
            print "Copying " + file
            try:
                self.net_copy(file_path, remote_dest_folder)
            except WindowsError:
                print 'could not connect to ', self.ip
            except IOError:
                print 'One of the files is being used on ', self.ip, ', skipping the copy procedure'

    def net_delete(self, path):
        """ Deletes files or directories on a remote computer. """
        if self.username == '':
            os.remove(path)

        else:
            self._wnet_connect()

            path = self._covert_unc(path)
            if os.path.exists(path):
                # Delete directory tree if object is a directory.
                if os.path.isfile(path):
                    os.remove(path)
                else:
                    shutil.rmtree(path)
            else:
                # Remove anyway if non-existent so as to raise an error.
                os.remove(path)


if __name__ == "__main__":
    main()
