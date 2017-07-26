# -*- coding: iso-8859-1 -*-
""" author : Jean-Christophe Clavier
    For some people, thunderbird lacks of a powerfull automatic detach function that keeps the link
    to the detached file from the mail itself (like Eudora has).
    Some plugins exists but there is now way to detach a document and replace it with a link to it's
    new location.
    For security reasons, the developper team doesn't want to allow the opening of a local file from
    thunderbird.
    When you have to keep large history of your emails, this may become a real problem for the size
    of your box and the facilities to automate some tasks on files (you can't use programs to see if
    you have doubles and so on).
    If, like me, you want to keep your email box as slim as possible by detaching attached documents
    and keep links to the detached files, this may be for you.

    The trick is that the file is detached and replaced by an html one in which you'll find the link
    to the file. The html file will be opened in your browser where the link to your local
    filesystem will operate.

    To keep it possible to change your detached files directory location, I have chosen to make the
    links with javascript (<a href="javascript:detachFile(file)">...). The javascript file name and
    location is a parameter of this script but will have to stay in the place you've decided.
    This way, the javascript must stay the same place but all the detached files may move without
    breaking the links with the mails (you'll just have to change the javascript)
    The best would be to read some environment variable from an embeded javascript so that the js
    script would not be fixed in some place forever but i don't know how to do that. If someone has
    an idea, i would be glad to know how

    The prm class is used to store the parameters
"""
import os, os.path, pprint, fnmatch, re, time, sys, traceback
import email, email.Utils, mimetypes, email.MIMEText
import quopri

class prm(object):
    """ Used to simply store parameters

        this could be in some kind of ini file but i wanted to keep this short
    """
    TEST=False # If True, the module just lists directories without detaching docs
    jsfile="C:\\Documents and Settings\\__User__\\Application Data\\Thunderbird\\Profiles\\__User__\\detach.js"  # The JS script used to open files
                    # (I use an external jsscript to ease the work in case one wants to change the detached files directory:
                    # only this script is to change)
    maildir="C:\\Documents and Settings\\__User__\\Application Data\\Thunderbird\\Profiles\\__User__\\Mail\\pop.__Fai__.fr" # The root dir of the mails
    outdir="C:\\Some\\Path\\You\\Want"                                               # The root dir where to put the modified Thunderbird files
    attachedFilesDir="C:\\Some\\Other\\Path\\To\\Your\\attached\\Files\\Dir"         # Where to put the attached files
    httpAttachedFilesDir="file:///C|/Some/Other/Path/To/Your/attached/Files/Dir/"    # What to use in your links (you may use a http server if you like)
                    # This will be used in the javascript function
    includeFiles=[]  # We want to detach docs only for these files (empty=all files)
    excludeFiles=["Trash"]  # We don't want to detach docs for these files
    includeDirs=[]  # We want to detach docs only for these dirs (empty=all dirs)
    excludeDirs=["Trash.sbd"]  # We don't want to detach docs for these dirs

    logfilename="gestmail.log"

class gestMail(object):
    """ Processes the mail directory
    """
    def __init__(self):
        self.lf=file(prm.logfilename,'w')

    def __del__(self):
        self.lf.close()

    def writeJS(self):
        jsScript="""
function openFile(file) {
    window.open("file:///%s/" + file, "_self")
}""" % prm.attachedFilesDir.replace("\\", "/").replace(":", "|")
        f=file(prm.jsfile,'w')
        f.write(jsScript)
        f.close()

    def writelog(self, *msg):
        sep=""
        for m in msg:
            print m.decode('latin1').encode('cp850', 'replace'), # display in M$ Windows command.
            self.lf.write("%s%s" % (sep, str(m)))
            sep=" "
        print ""
        self.lf.write("\n")

    def getfiles(self, dir):
        """ Walk throught the dir where mails are stored
        """
        for (dirpath, dirnames, filenames) in os.walk(dir):
            subdir=self.getSubdir(dir, dirpath)
            if  (prm.includeDirs==[] or subdir in prm.includeDirs) and subdir not in prm.excludeDirs:
                for file in [filenames[i] for i in range(len(filenames)) if not fnmatch.fnmatch(filenames[i], '*.msf')]:
                    if (prm.includeFiles==[] or file in prm.includeFiles) and file not in prm.excludeFiles:
                        self.writelog("-"*78)
                        self.writelog(os.path.join(subdir, file))
                        yield (dirpath, file)
            else:
                for e in dirnames[:]:
                    dirnames.pop()

    def getSubdir(self, rootdir, currentdir):
        subdir=currentdir[len(rootdir):]
        if len(subdir) > 0 and subdir[0] in ("\\", "/"):
            subdir=subdir[1:]
        return subdir

    def getHtmlLinksFileContent(self, filenames):
        """ returns the template of the html doc with the links
        """
        links=''
        for i, filename in enumerate(filenames):
            try:
                if len(filenames) > 1:
                    if i==0:
                        links+='<p><a href="javascript:openFile(\'%s\')">%s</a> - Existe déjà</p>\n' % (filename, filename)
                    else:
                        links+='<p>Renommé en <a href="javascript:openFile(\'%s\')">%s</a></p>\n' % (filename, filename)
                else:
                    links+='<p><a href="javascript:openFile(\'%s\')">%s</a></p>\n' % (filename, filename)
            except:
                self.writelog(filenames, filename)
                raise
        txt="""
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
  <meta http-equiv="Content-Type" content="text/html;charset=ISO-8859-1">
  <script type="text/javascript" src="file:///%s"></script>
</head>
<body>
%s
</body>
</html>
""" % (prm.jsfile.replace(":","|"), links)
        return txt

    def decode_Q(self, s):
        """ Decodes the file names when special characters are used (thanks to wacky)
        """
        try:
            qstart = s.index("=?") # Find the start of the Q-encoded string
            qend = s.index("?=", qstart + 2) # Find the end of it
            qenc_start = s.index("?", qstart + 2) # Find the encoding start
            qenc_end = s.index("?", qenc_start + 1) # Find the encoding end
            if s[qenc_start:qenc_end+1].upper() == "?Q?": # Q-encoded?
                enc = s[qstart+2:qenc_start] # Get the character encoding
                deQ = s[:qstart] # Get everything before the Q-encoded portion
                Qstring = s[qenc_end+1:qend] # Get the Q-encoded portion
                deQ += quopri.decodestring(Qstring, True).decode(enc) # Decode it
                deQ += s[qend+2:] # Get everything after the Q-encoded portion
                return self.decode_Q(deQ) # De-Q-code any further Q-encoded portions
            else:
                raise Exception("String is not Q-encoded: %s" % s) # It blew up
        except ValueError: # Index not found in string <s>; not Q-encoded
            return s # Returns a Unicode string

    def detachFile(self, att_name, filecontent, date=None):
        """ Writes the file and return the corresponding html

            The html file will store a link to the detached file
            If the file already exists, we compute a new name and create a link to the computed name file
            and to the file that has the same name...
            date is the date to use for the detached file
        """
        att_name=os.path.split(att_name)[1] # sometimes, the name of the attached file contains the whole path which is not wanted
        if att_name.find('=?') != -1: # If the filename is encoded, we decode it
            filename=quopri.decodestring(self.decode_Q(att_name).encode('latin1')) # and encode it in latin1 (you may change this to utf-8)
        else:
            filename=att_name
        filelist=[filename] # 
        # we write the attached file
        # Sometimes, due to formating, we find \n, \r or \t characters in the filenames. So we cut them off
        ofname=os.path.join(prm.attachedFilesDir, filename.strip().replace('\n','').replace('\r','').replace('?','').expandtabs(0))
        if os.path.exists(ofname):
            i=1
            fname=ofname
            sfname=os.path.splitext(fname)
            while os.path.exists(fname):
                fname="%s[%d]%s" % (sfname[0], i, sfname[1])
                i+=1
            filelist.append(os.path.split(fname)[-1])
            ofname=fname # the outfile name is the new one
        of=open(ofname,'wb')
        of.write(filecontent)
        of.close()
        if date:
            os.utime(ofname, (date, date))
        return self.getHtmlLinksFileContent(filelist)

    def processMessage(self, m):
        """ walk through the parts of multiparts MIME messages
        """
        self.writelog("    - process mail : ", re.compile("=\?.*?Q\?").sub("", quopri.decodestring(m.get_all("Subject")[0])))
        for i in m.walk():
            if i.is_multipart():
                continue
            if i.get_content_maintype() == 'text':
                pl = i.get_payload(decode=False)
                continue
            att_name = i.get_filename(None)  # get the filename
            if not att_name:
                # This part is relative to an attached file without name
                ext = mimetypes.guess_extension(i.get_content_type())
                att_name = 'makeitup%s' % ext
                pl = i.get_payload(decode=False) # Get the content of this part of the message without decoding it
            else:
                # This part is relative to an attached file
                ext=att_name.split(".")[-1]
                if ext != "html": # we dont detach html files because our links will be contained in html files
                                  # So, if whe use this script more than once, we don't want to detach html links files
                    pl = i.get_payload(decode=True) # We get the content of this part of the message and decode it
                    date=self.getDate(m.get_all("Date")[0])
                    htmlcontent=self.detachFile(att_name, pl, date)
                    # We replace the header to mention this is an html file
                    i.set_type("text/html")
                    try:
                        i.replace_header("Content-Transfer-Encoding", "7bit")
                    except KeyError:
                        self.writelog("ERROR - Content-Transfer-Encoding")
                        traceback.print_exc(file=self.lf)
                    i.replace_header("Content-Disposition", 'inline; filename="%s.html"' % att_name)
                    i.del_param("name")
                    # We replace the original included file by the html file containing the links
                    i.set_payload(htmlcontent)
        return str(m)

    def getDate(self, date):
        signe=re.compile(" [+-]")
        fuseau=signe.split(date.replace("GMT","").strip())
        tdate=list(time.strptime(fuseau[0], "%a, %d %b %Y %H:%M:%S"))
        try:
            decalage=int(fuseau[1])/100
            #print date, "*%s*" % signe.search(date).group(0)
            if signe.search(date).group(0)==" +":
                tdate[3]+=decalage
            elif signe.search(date).group(0)==" -":
                tdate[3]-=decalage
        except IndexError:
            pass
        # newdate=time.strftime("%d/%m/%Y %H:%M:%S", tdate)
        newdate=time.mktime(tdate)
        return newdate

    def process(self):
        # we open all the files containing emails
        try:
            for path, filename in self.getfiles(prm.maildir):
                if not prm.TEST:
                    f=file(os.path.join(path,filename),'r')
                    # we separate all the messages contained in the file
                    lmsg=f.read().split("From - ")
                    # we turn the messages into strings
                    msgs=[email.message_from_string("From - " + msg) for msg in lmsg[1:]]
                    # we write the out files
                    curdir=os.path.join(prm.outdir, self.getSubdir(prm.maildir, path))
                    if not os.path.exists(curdir):
                        os.makedirs(curdir)
                    curfile=os.path.join(curdir, filename)
                    of=file(curfile,'w')
                    for msg in msgs:
                        try:
                            of.write("%s\n" % self.processMessage(msg))
                        except:
                            of.write(str(msg))
                            self.writelog("ERROR while detaching - File is kept in the email")
                            traceback.print_exc(file=self.lf)
                    of.close()
        except:
            self.writelog("Fatal ERROR")
            traceback.print_exc(file=self.lf)
            raise

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('latin1') # Encoding problems have been very painful
        # This is not very clean and may cause trouble for you, i don't know
        # If someone knows a better way to manage encoding in this module, i would
        # be glad to know too...
    g=gestMail()
    g.writeJS()
    g.process()
