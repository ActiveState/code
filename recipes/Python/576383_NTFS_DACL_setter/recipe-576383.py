import os
import sys
import time
import subprocess
import active_directory

def set_perms(username):
    return subprocess.Popen(['fileacl', r'd:\users\%s' % username, '/S', r'%s:F' % username,
                             '/REPLACE', '/PROTECT'], stderr=subprocess.PIPE, stdout=subprocess.PIPE).communicate()

def get_users():
    return [str(user.cn) for user in active_directory.search ("objectCategory='Person'", "objectClass='User'")]

if __name__ == '__main__':
    while True:
        logfile = open('userperms_log.txt', 'a')
        logfile.write('\n\n\n' + time.ctime(time.time()) + '\n')
        sys.stdout = logfile
        for user in get_users():
            results = '\n'.join(list(set_perms(user)))
            if 'Error Bad trustee' in results:
                print results, '\n'
        logfile.close()
        time.sleep(5)
