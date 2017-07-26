#!/usr/bin/env python

## Copy files unattended over SSH using a glob pattern.
## It tries first to connect using a private key from a private key file
## or provided by an SSH agent. If RSA authentication fails, then 
## password login is attempted.

##
## DEPENDENT MODULES:
##      * paramiko, install it with `easy_install paramiko`

## NOTE: 1. The script assumes that the files on the source
##       computer are *always* newer that on the target;
##       2. no timestamps or file size comparisons are made
##       3. use at your own risk

hostname = '10.0.43.4' # remote hostname where SSH server is running
port = 22
username = 'myssh-username'
password = 'myssh-password'
rsa_private_key = r"/home/paramikouser/.ssh/rsa_private_key"

dir_local='/home/paramikouser/local_data'
dir_remote = "remote_machine_folder/subfolder"
glob_pattern='*.*'

import os
import glob
import paramiko
import md5

def agent_auth(transport, username):
    """
    Attempt to authenticate to the given transport using any of the private
    keys available from an SSH agent or from a local private RSA key file (assumes no pass phrase).
    """
    try:
        ki = paramiko.RSAKey.from_private_key_file(rsa_private_key)
    except Exception, e:
        print 'Failed loading' % (rsa_private_key, e)

    agent = paramiko.Agent()
    agent_keys = agent.get_keys() + (ki,)
    if len(agent_keys) == 0:
        return

    for key in agent_keys:
        print 'Trying ssh-agent key %s' % key.get_fingerprint().encode('hex'),
        try:
            transport.auth_publickey(username, key)
            print '... success!'
            return
        except paramiko.SSHException, e:
            print '... failed!', e

# get host key, if we know one
hostkeytype = None
hostkey = None
files_copied = 0
try:
    host_keys = paramiko.util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
except IOError:
    try:
        # try ~/ssh/ too, e.g. on windows
        host_keys = paramiko.util.load_host_keys(os.path.expanduser('~/ssh/known_hosts'))
    except IOError:
        print '*** Unable to open host keys file'
        host_keys = {}

if host_keys.has_key(hostname):
    hostkeytype = host_keys[hostname].keys()[0]
    hostkey = host_keys[hostname][hostkeytype]
    print 'Using host key of type %s' % hostkeytype

# now, connect and use paramiko Transport to negotiate SSH2 across the connection
try:
    print 'Establishing SSH connection to:', hostname, port, '...'
    t = paramiko.Transport((hostname, port))
    t.start_client()

    agent_auth(t, username)

    if not t.is_authenticated():
        print 'RSA key auth failed! Trying password login...'
        t.connect(username=username, password=password, hostkey=hostkey)
    else:
        sftp = t.open_session()
    sftp = paramiko.SFTPClient.from_transport(t)

    # dirlist on remote host
#    dirlist = sftp.listdir('.')
#    print "Dirlist:", dirlist

    try:
        sftp.mkdir(dir_remote)
    except IOError, e:
        print '(assuming ', dir_remote, 'exists)', e

#    print 'created ' + dir_remote +' on the hostname'

    # BETTER: use the get() and put() methods
    # for fname in os.listdir(dir_local):

    for fname in glob.glob(dir_local + os.sep + glob_pattern):
        is_up_to_date = False
        if fname.lower().endswith('xml'):
            local_file = os.path.join(dir_local, fname)
            remote_file = dir_remote + '/' + os.path.basename(fname)

            #if remote file exists
            try:
                if sftp.stat(remote_file):
                    local_file_data = open(local_file, "rb").read()
                    remote_file_data = sftp.open(remote_file).read()
                    md1 = md5.new(local_file_data).digest()
                    md2 = md5.new(remote_file_data).digest()
                    if md1 == md2:
                        is_up_to_date = True
                        print "UNCHANGED:", os.path.basename(fname)
                    else:
                        print "MODIFIED:", os.path.basename(fname),
            except:
                print "NEW: ", os.path.basename(fname),

            if not is_up_to_date:
                print 'Copying', local_file, 'to ', remote_file
                sftp.put(local_file, remote_file)
                files_copied += 1
    t.close()

except Exception, e:
    print '*** Caught exception: %s: %s' % (e.__class__, e)
    try:
        t.close()
    except:
        pass
print '=' * 60
print 'Total files copied:',files_copied
print 'All operations complete!'
print '=' * 60
