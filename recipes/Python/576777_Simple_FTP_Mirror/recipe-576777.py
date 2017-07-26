#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#       sfm.py - Simple FTP Mirror
#       
#       Copyright (c) 2009 joonis new media
#       Author: Thimo Kraemer <thimo.kraemer@joonis.de>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

"""
Usage: sfm [-v] [-q] [-u username [-p password [-a account]]]
        store|retrieve|remove|info hostname[:port] [remotedir [localdir]]
-v: verbose (-vvv debug)
-q: quiet
-u username: ftp username (default anonymous)
-p password: ftp password
-a account: ftp account
store: mirror the content of localdir to remotedir
retrieve: mirror the content of remotedir to localdir
remove: remove remotedir recursively
info: prints some information about remote mirror
hostname[:port]: remote host
remotedir: remote directory (default initial)
localdir: local directory (default current)

Example: sfm -u myuser store ftp.mydomain.com /myfolder /my/folder
         Will mirror the content of local directory /my/folder
         to remote directory /myfolder
"""

import sys
import os
import getopt
import getpass
import ftplib
import time
import datetime
import StringIO

globals = {
    'verbose': 1,
    'status': {
        'dirs_total': 0,
        'dirs_created': 0,
        'dirs_removed': 0,
        'files_total': 0,
        'files_created': 0,
        'files_updated': 0,
        'files_removed': 0,
        'bytes_transfered': 0,
        'bytes_total': 0,
        'time_started': datetime.datetime.now(),
        'time_finished': 0,
        },
    }

def log(msg, level=1, abort=False):
    if level <= globals['verbose'] or abort:
        if abort:
            sys.stdout = sys.stderr
            print
        print msg
    if abort:
        sys.exit(1)

def strfbytes(value):
    units = ['Bytes', 'KB', 'MB', 'GB', 'TB']
    value = float(value)
    for unit in units:
        if value < 1024: break
        value = value / 1024
    if unit == units[0]: fmt = '%.0f %s'
    else: fmt = '%.2f %s'
    return fmt % (value, unit)


class localHandler:
    """ Local file and directory functions"""
    def __init__(self, ftp, root):
        self.ftp = ftp
        self.root = root
        self.host = ''
    
    def storefile(self, src, dst):
        fh = open(dst, 'wb')
        self.ftp.retrbinary('RETR %s' % src, fh.write)
        fh.close()
    
    def storetext(self, text, dst):
        fh = open(dst, 'w')
        fh.write(text)
        fh.close()
    
    def readlines(self, path):
        fh = open(path, 'r')
        buffer = [line.strip() for line in fh.readlines()]
        fh.close()
        return buffer
    
    def list(self, dir, skip_mtime=False):
        dirs = []
        files = {}
        for name in os.listdir(dir):
            path = os.path.join(dir, name)
            if os.path.isdir(path):
                dirs.append(name)
            else:
                if skip_mtime: mtime = 0
                else: mtime = os.path.getmtime(path)
                files[name] = {
                    'size': os.path.getsize(path),
                    'mtime': mtime,
                    }
        return (dirs, files)
    
    def makedir(self, path):
        log('--> Create directory %s' % path, 2)
        os.mkdir(path)
        globals['status']['dirs_created'] += 1
    
    def removefile(self, path):
        log('--> Remove file %s' % path, 2)
        os.remove(path)
        globals['status']['files_removed'] += 1
    
    def removedir(self, dir):
        for name in os.listdir(dir):
            path = os.path.join(dir, name)
            if os.path.isdir(path):
                self.removedir(path)
            else:
                self.removefile(path)
        log('--> Remove directory %s' % dir, 2)
        os.rmdir(dir)
        globals['status']['dirs_removed'] += 1


class remoteHandler:
    """Remote file and directory functions"""
    def __init__(self, ftp, root):
        self.ftp = ftp
        self.root = root
        self.host = ftp.host
    
    def storefile(self, src, dst):
        fh = open(src)
        self.ftp.storbinary('STOR %s' % dst, fh)
        fh.close()
    
    def storetext(self, text, dst):
        fh = StringIO.StringIO(text)
        self.ftp.storlines('STOR %s' % dst, fh)
        fh.close()
    
    def readlines(self, path):
        buffer = []
        self.ftp.retrlines('RETR %s' % path, buffer.append)
        return buffer
    
    def list(self, dir, skip_mtime=False):
        month_to_int = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4,
            'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9,
            'Oct': 10, 'Nov': 11, 'Dec': 12}
        try:
            buffer = []
            self.ftp.dir('-a ', dir, buffer.append)
        except ftplib.error_temp:
            buffer = []
            self.ftp.dir(dir, buffer.append)
        dirs = []
        files = {}
        for line in buffer:
            cols = line.split(None, 8)
            name = os.path.split(cols[8])[1]
            if cols[0] == 'total' or name in ('.', '..'):
                continue
            if cols[0].startswith('d'):
                dirs.append(name)
            else:
                if skip_mtime:
                    mtime = 0
                else:
                    month = month_to_int[cols[5]]
                    day = int(cols[6])
                    if cols[7].find(':') == -1:
                        year = int(cols[7])
                        hour = minute = 0
                    else:
                        year = datetime.date.today().year
                        hour, minute = [int(s) for s in cols[7].split(':')]
                    mtime = datetime.datetime(year, month, day, hour, minute)
                    mtime = int(time.mktime(mtime.timetuple()))
                size = int(cols[4])
                files[name] = {
                    'size': size,
                    'mtime': mtime,
                    }
        return (dirs, files)
    
    def makedir(self, path):
        log('--> Create directory %s' % path, 2)
        self.ftp.mkd(path)
        globals['status']['dirs_created'] += 1
    
    def removefile(self, path):
        log('--> Remove file %s' % path, 2)
        self.ftp.delete(path)
        globals['status']['files_removed'] += 1
    
    def removedir(self, path):
        dirs, files = self.list(path)
        for dir in dirs:
            self.removedir(os.path.join(path, dir))
        for file in files:
            self.removefile(os.path.join(path, file))
        if path == '/':
            return
        log('--> Remove directory %s' % path, 2)
        self.ftp.rmd(path)
        globals['status']['dirs_removed'] += 1


def mirror(src, dst, subdir=''):
    src_path = os.path.normpath('%s/%s' % (src.root, subdir))
    dst_path = os.path.normpath('%s/%s' % (dst.root, subdir))
    log('Working on %s%s' % (src.host, src_path))
    
    src_dirs, src_files = src.list(src_path)
    if '.sfmstat' in src_files:
        del src_files['.sfmstat']
    
    globals['status']['dirs_total'] += len(src_dirs)
    globals['status']['files_total'] += len(src_files)
    
    dst_dirs, dst_files = dst.list(dst_path, True)
    if '.sfmstat' in dst_files:
        sfmstat = dst.readlines(os.path.join(dst_path, '.sfmstat'))
        del dst_files['.sfmstat']
    else:
        if dst_path == dst.root and (dst_dirs or dst_files):
            if globals['verbose']: abort = False
            else: abort = True
            log('New mirror, but target directory not empty!', abort=abort)
            result = raw_input('Do you really want to replace this directory? [y|n]: ')
            if result.lower() not in ('y', 'yes'):
                log('Aborted', abort=True)
        sfmstat = ['0 %s%s' % (src.host, src_path)]
    
    last_updated, mirror_path = sfmstat[0].split(None, 1)
    if mirror_path != (src.host + src_path):
        if globals['verbose']: abort = False
        else: abort = True
        error = 'Mirror mismatch!\n%s already contains another mirror of %s' % (dst_path, mirror_path)
        log(error, abort=abort)
        result = raw_input('Do you really want to replace this mirror? [y|n]: ')
        if result.lower() not in ('y', 'yes'):
            log('Aborted', abort=True)
        sfmstat = ['0 %s%s' % (src.host, src_path)]
    
    for line in sfmstat[1:]:
        mtime, file = line.split(None, 1)
        if file in dst_files:
            dst_files[file]['mtime'] = int(mtime)
    
    for dir in dst_dirs:
        if dir not in src_dirs:
            path = os.path.join(dst_path, dir)
            log('-> Remove directory %s' % path)
            dst.removedir(path)
    
    for file in dst_files:
        if file not in src_files:
            dst_file = os.path.join(dst_path, file)
            log('-> Remove file %s: %s' % (dst_file, strfbytes(dst_files[file]['size'])))
            dst.removefile(dst_file)
    
    newstat = ['%i %s%s' % (int(time.time()), src.host, src_path)]
    for file in src_files:
        if file not in dst_files or src_files[file]['mtime'] > dst_files[file]['mtime'] or src_files[file]['size'] != dst_files[file]['size']:
            src_file = os.path.join(src_path, file)
            dst_file = os.path.join(dst_path, file)
            if file in dst_files:
                log('-> Update file %s: %s' % (dst_file, strfbytes(src_files[file]['size'])))
                globals['status']['files_updated'] += 1
            else:
                log('-> Create file %s: %s' % (dst_file, strfbytes(src_files[file]['size'])))
                globals['status']['files_created'] += 1
            dst.storefile(src_file, dst_file)
            globals['status']['bytes_transfered'] += src_files[file]['size']
        globals['status']['bytes_total'] += src_files[file]['size']
        newstat.append('%i %s' % (src_files[file]['mtime'], file))
    dst.storetext('\n'.join(newstat), os.path.join(dst_path, '.sfmstat'))
    
    for dir in src_dirs:
        if dir not in dst_dirs:
            dst_dir = os.path.join(dst_path, dir)
            log('-> Create directory %s' % dst_dir)
            dst.makedir(dst_dir)
        mirror(src, dst, os.path.join(subdir, dir))


def info(remote):
    try:
        sfmstat = remote.readlines(os.path.join(remote.root, '.sfmstat'))
    except ftplib.error_perm, err:
        if not err[0].startswith('550'):
            log(err, abort=True)
        sfmstat = None
    print
    if sfmstat:
        last_updated, mirror_path = sfmstat[0].split(None, 1)
        last_updated = datetime.datetime.fromtimestamp(float(last_updated))
        print 'Mirror of', mirror_path
        print last_updated.strftime('Last updated on %A, %d. %B %Y at %H:%M:%S')
    else:
        print 'No mirror recognized'
    print
    print 'Content of %s%s:' % (remote.host, remote.root)
    remote.ftp.dir(remote.root)
    print


def remove(remote):
    if globals['verbose']:
        info(remote)
        result = raw_input('Do you really want to remove this directory? [y|n]: ')
        if result.lower() not in ('y', 'yes'):
            log('Aborted', abort=True)
    remote.removedir(remote.root)


def main():
    username = ''
    password = ''
    account = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'vqu:p:a:')
    except getopt.GetoptError, msg:
        log('%s\n%s' % (msg, __doc__), abort=True)
    for opt, val in opts:
        if opt == '-v': globals['verbose'] += 1
        if opt == '-q': globals['verbose'] = 0
        if opt == '-u': username = val
        if opt == '-p': password = val
        if opt == '-a': account = val
    
    if not args:
        log('No action given\n' + __doc__, abort=True)
    
    action = args[0]
    if action not in ('store', 'retrieve', 'remove', 'info'):
        log('Unknown action: %s\n%s' % (action, __doc__), abort=True)
    
    if len(args) == 1:
        log('Missing hostname\n' + __doc__, abort=True)
    
    args[1] = args[1].split(':')
    host = args[1][0]
    if len(args[1]) == 1:
        port = 21
    else:
        port = int(args[1][1])
    
    remotedir = '/'
    if len(args) > 2:
        remotedir = os.path.normpath(args[2])
        if not remotedir.startswith('/'):
            log('Invalid remotedir, must start with /', abort=True)
    
    localdir = os.getcwd()
    if len(args) > 3:
        if action not in ('store', 'retrieve'):
            log('Too many arguments\n%s' % __doc__, abort=True)
        localdir = os.path.abspath(args[3])
        if not os.path.isdir(localdir):
            log('localdir does not exist: %s' % localdir, abort=True)
    
    if len(args) > 4:
        log('Too many arguments\n%s' % __doc__, abort=True)
    
    if not username:
        username = 'anonymous'
    elif not password and globals['verbose']:
        password = getpass.getpass('FTP Password: ')
    
    ftp = ftplib.FTP()
    if globals['verbose'] > 2:
        ftp.set_debuglevel(globals['verbose']-2)
    ftp.connect(host, port)
    ftp.login(username, password, account)
    try:
        ftp.cwd(remotedir)
    except ftplib.error_perm, err:
        if err[0].startswith('550'):
            log('remotedir does not exist: %s' % remotedir, abort=True)
        else:
            raise
    ftp.cwd('/')
    
    local = localHandler(ftp, localdir)
    remote = remoteHandler(ftp, remotedir)
    
    if action == 'store':
        mirror(local, remote)
    elif action == 'retrieve':
        mirror(remote, local)
    elif action == 'remove':
        remove(remote)
    elif action == 'info':
        info(remote)
        ftp.quit()
        return
    
    ftp.quit()
    log('Done')
    status = globals['status']
    status['time_finished'] = datetime.datetime.now()
    print
    print '=' * 60
    print 'Processing Summary'
    print '=' * 60
    print '%-30s%30s' % ('Directories created', status['dirs_created'])
    print '%-30s%30s' % ('Directories removed', status['dirs_removed'])
    print '%-30s%30s' % ('Directories total', status['dirs_total'])
    print
    print '%-30s%30s' % ('Files created', status['files_created'])
    print '%-30s%30s' % ('Files updated', status['files_updated'])
    print '%-30s%30s' % ('Files removed', status['files_removed'])
    print '%-30s%30s' % ('Files total', status['files_total'])
    print
    print '%-30s%30s' % ('Bytes transfered', strfbytes(status['bytes_transfered']))
    print '%-30s%30s' % ('Bytes total', strfbytes(status['bytes_total']))
    print
    print '%-30s%30s' % ('Time started', status['time_started'])
    print '%-30s%30s' % ('Time finished', status['time_finished'])
    print '%-30s%30s' % ('Duration', status['time_finished']-status['time_started'])
    print '=' * 60
    print


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        log('Aborted', abort=True)
    except SystemExit:
        raise
    except Exception, err:
        log(err, abort=True)
