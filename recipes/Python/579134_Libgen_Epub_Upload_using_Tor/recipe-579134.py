import glob
import os
import time
import bs4
import socks
import socket
import magic
import random
import hashlib

# Tor proxy
def create_connection(address, timeout=None, source_address=None):
    sock = socks.socksocket()
    sock.connect(address)
    return sock

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
socket.socket = socks.socksocket
socket.create_connection = create_connection

import mechanize

br = mechanize.Browser()

#br.set_debug_http(True)
#br.set_debug_redirects(True)
#br.set_debug_responses(True)

checkmd5url = "http://libgen.io/foreignfiction/index.php?md5="
uploadurl = "http://libgen.io/foreignfiction/librarian"
username = "genesis"
password = "upload"

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

br.add_password(uploadurl, username, password)

for filename in sorted(glob.glob("*.epub")):
    print "File : %s" % filename

    # Getting mimetype
    with magic.Magic(flags=magic.MAGIC_MIME_TYPE) as m:
        mimetype = m.id_filename(filename)

    filesize = os.stat(filename).st_size

    # Calculating MD5 hash
    digester = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            digester.update(chunk)
    md5sum = digester.hexdigest()

    # Check if MD5 is already in DB
    response = br.open(checkmd5url + md5sum)
    soup = bs4.BeautifulSoup(response.read())
    fonts = soup.find_all('font')
    foundmd5 = True
    for font in fonts:
        if font.get_text().strip() == "Found 0  results":
            foundmd5 = False
            break
    if foundmd5:
        print "Already in DB : %s" % filename      
        continue

    # Uploading
    br.open(uploadurl)
    br.select_form(nr=0)
    br.form.add_file(open(filename), mimetype, filename, name='uploadedfile')
    #~ print br.form
    response = br.submit()

    # Registering after upload
    try:
        br.select_form(nr=1)
    except mechanize.FormNotFoundError as fnfe:
        print response.read()
        continue

    # Fixing required data
    br.form.set_all_readonly(False)
    if br.form["authorfamily1"] == "":
        if br.form["authorsurname1"] != "":
            # Surname is present
            br.form["authorfamily1"] = br.form["authorsurname1"]
            br.form["authorsurname1"] = ""
        else:
            # Only name present
            br.form["authorfamily1"] = br.form["authorname1"]
            br.form["authorname1"] = ""

    response = br.submit()

    # Reading registration response
    soup = bs4.BeautifulSoup(response.read())
    h1s = soup.find_all('h1')
    if len(h1s) == 1:
        print h1s[0].get_text().strip()
    else:
        print soup.prettify()

    # Cooldown
    time.sleep(random.randint(1,9))
