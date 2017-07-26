from __future__ import print_function, unicode_literals

import win32com.client
import codecs

FILE = 1
DRAFT = 4

def login(user, password):
    app = win32com.client.Dispatch('NovellGroupWareSession')
    account = app.MultiLogin(user, None, password, 1)
        # 0 - promptIfNeeded
        # 1 - noverPrompt
        # 2 - allowPasswordPrompt

def incoming(account):
    return account.MailBox.Messages.Find('(mail) and (box_type = incoming)')

def msg_atts(msg):
    'att generator'
    for att in msg.Attachments:
        if att.ObjType == FILE:
            fn = att.FileName
            if not fn:
                continue
            elif fn == 'Mime.822':
                # email from Thunderbird through smtp
                continue
            elif fn == 'Header':
                # forwarded from Thunderbird through smtp
                continue
        yield att
    return None

def att_save(att, fpath):
    if att.AttachmentSize > 0:
        att.Save(fpath)
    else:
        # GW-error workaround, cat > fpath
        with open(fpath, 'wb'):
            pass

def msg_move(msg, fromFolder, toFolder):
    fromFolder.Messages.Move(msg, toFolder.Messages)

def msg_move2(msg, toFolder):
    'move from Inbox'
    inbox = msg.Parent.MailBox
    folders = msg.EnclosingFolders
    if inbox in folders:
        msg_move(msg, inbox, toFolder)
    elif not toFolder in folders:
        toFolder.Messages.Add(msg)
        
class AttStream:
    def __init__(self, att):
        self.stream = att.Stream
        self.size = att.AttachmentSize
    def read(self, size = -1):
        if size < 0:
            size = self.size
        data =  self.stream.Read(size)
        return str(data)
    def close(self):
        pass
        
def att_text(att, encoding):
    fp = AttStream(att)
    return fp.read().decode(encoding)
    
def att_reader(att, encoding):
    '''
    with att_reader(att, encoding) as fp:
        do_something
    '''
    fp = AttStream(att)
    return codecs.getreader(encoding)(fp)

def create_msg(folder):
    return folder.Messages.Add('GW.MESSAGE.MAIL', DRAFT)

def add_recipients(msg, *addrL):
    for addr in addrL:
        msg.Recipients.Add(addr)
    
def add_file(msg, fpath, fn = None):
    if fn:
        msg.Attachments.Add(fpath, FILE, fn)
    else:
        msg.Attachments.Add(fpath, FILE)
