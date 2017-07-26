#!/usr/bin/env python

import os
import urllib2
import urllib
import zipfile
import sys
import subprocess
import shutil
import pipes

## browser friendly pages
## http://commondatastorage.googleapis.com/chromium-browser-continuous/index.html
## http://commondatastorage.googleapis.com/chromium-browser-continuous/index.html?path=Win/
## Chrome Canary: https://tools.google.com/dlpage/chromesxs?platform=win
MBFACTOR = float(1<<20) # divisor to convert bytes to megabytes

# URL_PREFIX_CONTINUOUS = 'http://commondatastorage.googleapis.com/chromium-browser-continuous/'
# URL_PREFIX_SNAPSHOTS = 'http://commondatastorage.googleapis.com/chromium-browser-snapshots/'
# URL_PREFIX_OFFICIAL = 'http://commondatastorage.googleapis.com/chromium-browser-official/'

AVAILABLE_CHANELLS = {'continuous':'http://commondatastorage.googleapis.com/chromium-browser-continuous/',
						'snapshot':'http://commondatastorage.googleapis.com/chromium-browser-snapshots/',
						'official':'http://commondatastorage.googleapis.com/chromium-browser-official/'}

os_suffixes = dict(
	linux2=['Linux', 'linux'],
	linux64=['Linux_x64', 'linux64'],
	mac=['Mac', 'mac'],
	win32=['Win', 'win32']
)

def usage():
	os_list = "|".join([platform_[1] for platform_ in os_suffixes.values()])
	print '''Usage %s [%s] [%s]
	Default channell is: continuous
''' % (os.path.basename(sys.argv[0]), os_list, '|'.join(AVAILABLE_CHANELLS.keys()))

if len(sys.argv) > 1 and sys.argv[1].lower() in ['-h', '--help', '/?']:
	usage()
	sys.exit(-1)


platform = len(sys.argv) > 1 and sys.argv[1] or sys.platform

if platform == 'darwin':
	platform = 'mac'

channell = None

if len(sys.argv) > 2:
	channell = sys.argv[2]
	if channell not in AVAILABLE_CHANELLS.keys():
		print '\n***ERROR***:No such channell %s' % channell
		usage()
		sys.exit(-1)

if not channell:
	channell = 'continuous'

tmp = os.environ.get('TMP') or os.environ.get('TEMP') or '/tmp'

if sys.platform == 'win32':
	apps_folder = r'd:\Program Files'
if sys.platform == 'darwin':
    apps_folder = os.path.join(os.environ.get('HOME'), 'Applications')
else:
	apps_folder = os.path.join(os.environ.get('HOME'), 'bin')

def _reporthook2(count, blockSize, total_size, url=None):
	current_size = int(count*blockSize)
	sys.stdout.write("    %.2f MB  of  %.2f MB      \r" % (current_size/(MBFACTOR), total_size/MBFACTOR))

def download_binary_file(url, local_fname):
	print '''
Downloading
    %s
to
    %s...\n''' % (url, local_fname),
	if sys.stdout.isatty():
		urllib.urlretrieve(url, local_fname,lambda nb, bs, fs, url=url: _reporthook2(nb,bs,fs,url))
		sys.stdout.write('\n')
	else:
		urllib.urlretrieve(url, dst)

def extract_zip_file(zipFilePath, extractDir):
	if not os.path.exists(extractDir):
		os.mkdir(extractDir)	
	print '''Extracting
    %s 
to
    %s...''' % (zipFilePath, extractDir),
	zfile = zipfile.ZipFile(zipFilePath)

	uncompress_size = sum((file.file_size for file in zfile.infolist()))
	
	extracted_size = 0
	
	print '\n'
	for _file in zfile.infolist():
		extracted_size += _file.file_size
		sys.stdout.write("    %s%%\t\t%s\n" % (extracted_size * 100/uncompress_size, _file.filename))
		zfile.extract(_file, path=extractDir)
# ORIG 	zip.extractall(path=extractDir)
	print 'Ok'

def do_osx_install(srcdir, targetdir):
    
    if os.path.exists(targetdir):
        print 'Target dir %s already exists! Removing...'
        shutil.rmtree(targetdir)
    
    install_script = os.popen('find '+ srcdir +' -iname install.sh').read().strip()
    print 'DBG install_script:', install_script
    os.popen('chmod +x "%s"' % install_script)
    cmd_install = '%s %s %s' % (pipes.quote(install_script), srcdir, targetdir)
    print 'DBG cmd: "%s"' % cmd_install
    cmd_chmod_chromium = 'find %s -name Chromium -exec chmod +x {} \;' % (targetdir)
    cmd_chmod_chromium_helper = 'find %s -name Chromium\ Helper -exec chmod +x {} \;' % (targetdir)
    for cmd in [cmd_install, cmd_chmod_chromium, cmd_chmod_chromium_helper]:
        
        proc = subprocess.Popen(cmd, shell=True)
        proc.wait()
        if proc.returncode:
            print "returncode " + str(proc.returncode)

print '''
platform:\t%s
Unpacking to dir:\t%s
''' % (platform, apps_folder)

print 'Checking for latest version...',

try:
	os_suffix = os_suffixes[platform][0]
except KeyError:
	print '\n\nERROR:\tFirst arg should be platform name, one of: %s' % ', '.join(os_suffixes.keys())
	sys.exit(-1)

# use proxy if set as an ENV var
proxy = os.environ.get('HTTP_PROXY')
if proxy:
	protocol, host = proxy.split('://')
	print 'Using proxy', proxy
	http_proxy_handler = urllib2.ProxyHandler({protocol:host})
	opener = urllib2.build_opener(http_proxy_handler)
	urllib2.install_opener(opener)
else:
	opener = urllib2.build_opener()

opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24')]

print 'Probing last version...',
url_last_change = AVAILABLE_CHANELLS[channell] + os_suffix + '/LAST_CHANGE'
print url_last_change

version = opener.open(url_last_change).read().strip()
print 'Current version:', version

local_fname = os.path.join(tmp, 'chrome-%s_%s.zip' % (platform, version))

need_downloading = True

if os.path.exists(local_fname):
	print '\nFile %s already exists!\nRemove it? (Y/n)' % local_fname
	ans = raw_input()
	if ans.lower() != 'n':
		print 'Deleting existing file %s' % local_fname, 
		os.remove(local_fname)
		print 'Ok'
	else:
		need_downloading = False

url = AVAILABLE_CHANELLS[channell] + os_suffix + '/' + version + '/chrome-' + os_suffixes[platform][1] + '.zip'

print 'Downloading from:', url

if (sys.version_info.minor < 6):
	need_downloading and os.system('wget -c %s -O %s' % (url, local_fname))
	print 'Unzippping...'
	cmd = 'unzip -o %s -d "%s"' % (os.path.abspath(local_fname), apps_folder)
	print cmd
	os.system(cmd)
else:
	need_downloading and download_binary_file(url, local_fname)
	extract_zip_file(local_fname, apps_folder)

if (sys.platform=='darwin'):
    chrome_app_dir = os.path.join(apps_folder, 'chrome-mac')
    target_dir = os.path.join(apps_folder, 'Chromium')
    do_osx_install(chrome_app_dir, target_dir)
    # raw_input('removing unpacked chrome folder ' + chrome_app_dir)
    shutil.rmtree(chrome_app_dir)
        

print 'Done!'
