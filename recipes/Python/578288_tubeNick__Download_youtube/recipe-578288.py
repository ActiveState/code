#!/usr/bin/python3

# Name: tubeNick.py
# Version: 1.6
# Author: pantuts
# Description: Download videos from youtube.
# Use python3 and later.
# Agreement: You can use, modify, or redistribute this tool under 
# the terms of GNU General Public License (GPLv3). This tool is for educational purposes only.
# Any damage you make will not affect the author.
# Send bugs to above email.
# Usage: python3 tubeNick.py youtubeURLhere
# Download: https://sourceforge.net/projects/tubenickdownloa/

import re
import urllib.request
import urllib.error
import sys
import time

COLON = '%253A'
BACKSLASH = '%252F'
QMARK = '%253F'
EQUALS = '%253D'
AMPERSAND = '%2526'
PERCENT = '%2525'

MATCHED_LINK = []
SIGNATURE = []
COMPLETE_LINK = []
VIDEO_TYPE = []
VIDEO_RES = []
FINAL_LINK = []

sTUBE = ''
final_title = ''
final_url = ''
url = ''
final_f_format = 0
arg_queryf = ''
arg_format = ''
arg_f_format = []

########################################################################

def main():

    global url
    global arg_format
    global arg_queryf
    
    if len(sys.argv) < 2 or len(sys.argv) > 4: return usage()
    elif len(sys.argv) == 2:
        if sys.argv[-1] == '-h': return usage()
        else:
            if sys.argv[-1] == '-': url = list(sys.stdin.readlines())
            else: url = sys.argv[-1]
    elif len(sys.argv) == 3:
        for args in sys.argv:
            if '-h' in args or '-f' in args: print('\nCommand ERROR...'); exit(1)
        if sys.argv[1] == '-q': sys.argv[1] = '-q'; arg_queryf = sys.argv[1]
        else: return usage()
        if sys.argv[-1] == '-': url = list(sys.stdin.readlines())
        else: url = sys.argv[-1]
    elif len(sys.argv) == 4:
        for args in sys.argv:
            if '-h' in args or '-q' in args: print('\nCommand ERROR...'); exit(1)
        if sys.argv[1] == '-f': sys.argv[1] = '-f';
        else: return usage()
        arg_format = sys.argv[2]
        if sys.argv[-1] == '-': url = list(sys.stdin.readlines())
        else: url = sys.argv[-1]
    else: return usage()
   
    if sys.argv[-1] == '-':
        
        i = 0
        while i < len(url):
            check_url(url[i].split('\\')[0])
            i = i + 1
    else:
        check_url(url)
    
########################################################################

def usage():

    print('\nUSAGE: python3 tubeNick.py -q [-f format] [URL or [-] STDIN]')
    print('Optional arguments:')
    print('\t-q \t\tQuery video formats. Use of -f will be invalid.')
    print('\t-f format\tSupply queried format. Highest video if blank.')
    print('\t-h \t\tPrint this.')
    print()

########################################################################

def check_url(url):
    
    global final_url
    
    tmp_url = 'http://www.youtube.com/get_video_info?video_id='
    #invalid = '~`!@#$%^&*()_=+{[}]|\\:;"\'<,>.?/'
    tmp_id = ''
    final_id = ''
    eq = 0
    last_id = 0
    
    split_url = url.split('/')
    tmp_id = split_url[-1]
    
    if 'v' not in url: print('[-] URLError: Invalid link.'); exit(1)
    if len(url) < 20: print('[-] URLError: Invalid link.'); exit(1)
    if 'youtube.com' not in url and url != '-': print('[-] URLError: Youtube URLs only.'); exit(1)
    
    if 'watch?v=' in tmp_id:
        eq = tmp_id.index('=') + 1
        if '&' in tmp_id:
            tmp_split = tmp_id.split('&')[0]
            final_id = tmp_split[eq:]
        else: final_id = tmp_id[eq:]
    
    # the video id for requesting get_video_info
    final_url = tmp_url + final_id
    
    if final_url:
        con = 'Connecting...\n'
        i = 0
        while i < len(con):
            sys.stdout.write(con[i])
            sys.stdout.flush()
            time.sleep(0.01)
            i = i + 1
            
        connection(final_url)

########################################################################

def connection(final_url):

    global sTUBE
    
    try:
        req = urllib.request.Request(final_url)
        req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0')
        yTUBE = urllib.request.urlopen(req)
        sTUBE = str(yTUBE.read())
        
    except urllib.request.URLError as e: print(e.reason); exit(1)
    
    if sTUBE:
        rep_page(sTUBE)

########################################################################

def rep_page(sTUBE):

    REP_STR = [COLON, BACKSLASH, QMARK, EQUALS, AMPERSAND, PERCENT]
    if REP_STR[0] in sTUBE:
        sTUBE = sTUBE.replace('%253A', ':')
    if REP_STR[1] in sTUBE:
        sTUBE = sTUBE.replace('%252F', '/')
    if REP_STR[2] in sTUBE:
        sTUBE = sTUBE.replace('%253F', '?')
    if REP_STR[3] in sTUBE:
        sTUBE = sTUBE.replace('%253D', '=')
    if REP_STR[4] in sTUBE:
        sTUBE = sTUBE.replace('%2526', '&')
    if REP_STR[5] in sTUBE:
        sTUBE = sTUBE.replace('%2525', '%')
    
    crawl_youtube(sTUBE)
    
########################################################################

def crawl_youtube(sTUBE):

    global VIDEO_TITLE
    global MATCHED_LINK
    global SIGNATURE
    global COMPLETE_LINK
    global VIDEO_TYPE
    global VIDEO_RES
    global final_title
    global final_f_format
    global arg_f_format
    
    # get title
    vid_title = re.search(r'title=\w.+', sTUBE)
    if vid_title:
        the_title = vid_title.group()
        if '&' in the_title:
            tmp_title = the_title.index('&')
        else: tmp_title = len(the_title) - 1
        f_title = the_title[6:tmp_title]
        final_title = f_title.replace('+', ' ')
        for per_num in ['%21','%22','%23','%24','%25','%26','%27','%28','%29',\
        '%2D','%5F','%3D','%2B','%5B','%7B','%7D','%5D','%7C','%5C',\
        '%3A','%3B','%2C','%3C','%3E','%2E','%3F','%2F']:
            if per_num in final_title:
                final_title = final_title.replace(per_num, '')
    else: print('[-] ERROR: Can\'t find video title. Title set to default.'); final_title = 'DownloadYTube'
    
    # get links
    match = re.findall(r'http://\w.+?cp.+?video.+?quality.+?3D\w.+?%', sTUBE)
    if match:
        for mat in match:
        
            MATCHED_LINK.append(mat)
            
            # get signature
            find_sig = re.search(r'sig+\S.+quality', mat)
            if find_sig:
                c_sig = find_sig.group()
                final_sig = c_sig[6:-10]
                SIGNATURE.append(final_sig)
                #print(final_sig)
                
            # for link / get last characters [id]
            if 'id=' in mat:
                y_index = mat.index('id=')
                id_last = y_index + 19
                li = mat[:id_last]
                COMPLETE_LINK.append(li)
                
            # get video type
            if 'video/' in mat:
                vid_start = mat.index('video/')
                vid_end = vid_start + 11
                vid_type = mat[vid_start:vid_end]
                for vid_cod in ['flv', 'webm', 'mp4', '3gp']:
                    if vid_cod in vid_type:
                        VIDEO_TYPE.append(vid_cod)
                        
    else: print('[-] URLError'); exit(1)
                
    # get formats/resolution
    fmt = re.search(r'fmt_list=\S.+?\&', sTUBE)
    if fmt:
        frmt = fmt.group().split('%2F')
        for v_format in frmt:
            if 'x' in v_format:
                VIDEO_RES.append(v_format)
    else: print('Can\'t find video formats. '); exit(1)
    
    # append and combine video type and resolution
    j = 0
    while j < len(COMPLETE_LINK):
        arg_f_format.append(VIDEO_TYPE[j] + '_' + VIDEO_RES[j])
        j = j + 1
    
    # if argument is [ -q ]
    if arg_queryf:
        i = 0
        print(final_title)
        while i < len(COMPLETE_LINK):
            print('[+] ' + VIDEO_TYPE[i] + '_' + VIDEO_RES[i])
            time.sleep(0.04)
            i = i + 1
        flush()
        
    else:
            
        # if argument is [ -f ] and the default format
        if arg_format is not None and arg_format in arg_f_format:
            final_f_format = arg_f_format.index(arg_format)
        elif arg_format not in arg_f_format and len(sys.argv) != 2:
            print('' + arg_format + ' not in video formats. Setting to default format: ', arg_f_format[0])
            final_f_format = 0
        else:
            final_f_format = 0
        
        final_download_link()

########################################################################

def final_download_link():

    global FINAL_LINK
    
    i = 0
    while i < len(COMPLETE_LINK):
        FINAL_LINK.append(COMPLETE_LINK[i] + '&signature=' + SIGNATURE[i])
        i = i + 1
        
    download()
    
########################################################################

def download():

    req = urllib.request.Request(FINAL_LINK[final_f_format])
    req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0')
    try:
        tmp_req = urllib.request.urlopen(req)
        tmp_size = tmp_req.getheader('Content-Length')
        size = int(tmp_size)
        
        print('Downloading...')
        
        # for reporthook in urlretrieve, 3 arguments needed
        def download_progress(counter, bsize, size):
            prog_percent = (counter * bsize * 100) / size
            sys.stdout.write('\r' + final_title.replace(' ', '') + '.' + VIDEO_TYPE[final_f_format] + \
                    ' .......................... %2.f%%' % int(prog_percent))
            sys.stdout.flush()

        urllib.request.urlretrieve(FINAL_LINK[final_f_format], (final_title.replace(' ', '') + \
                    '.' + VIDEO_TYPE[final_f_format]), reporthook=download_progress)
        print('\nDone.')
        flush()
        
    except urllib.error.HTTPError as e: print('Error downloading : ' + e.reason); exit(1)
        
########################################################################

def flush():

    del MATCHED_LINK[:]
    del SIGNATURE[:]
    del COMPLETE_LINK[:]
    del VIDEO_TYPE[:]
    del VIDEO_RES[:]
    del FINAL_LINK[:]

    sTUBE = ''
    final_title = ''
    final_url = ''
    url = ''
    final_f_format = 0
    arg_queryf = ''
    arg_format = ''
    del arg_f_format[:]

########################################################################

if __name__ =='__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nExiting.')
