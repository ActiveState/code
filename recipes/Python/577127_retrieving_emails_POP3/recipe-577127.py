import email, StringIO

def list_(pop):
    resp, lst, octets = pop.list()
    return [i.split() for i in lst]
        # msgnum, msgsize

def retr_text(pop, msgnum):
    resp, msg, octets = pop.retr(msgnum)
    return b'\n'.join(msg)

def retr_msg(pop, msgnum):
    msg = retr_text(pop, msgnum)
    fp = StringIO.StringIO(msg)
    try:
        msg = email.message_from_file(fp)
    finally:
        fp.close()
    
def list_text(pop):
    'generator msgnum, text'
    for msgnum, msgsize in list_(pop):
        text = retr_text(pop, msgnum)
        yield msgnum, text

def list_msg(pop):
    'generator msgnum, msg'
    for msgnum, msgsize in list_(pop):
        msg = retr_msg(pop, msgnum)
        yield msgnum, msg
