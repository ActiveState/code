import itertools
import subprocess
import mailbox



def create_message(frm, to, content, headers = None):
    if not headers: 
        headers = {}
    m = mailbox.Message()
    m['from'] = frm
    m['to'] = to
    for h,v in headers.iteritems():
        m[h] = v
    m.set_payload(content)
    return m


def generate_content(prefix):
    return """%s
--
%s"""%(prefix, subprocess.Popen(["/usr/games/fortune"], stdout=subprocess.PIPE).stdout.read())


def main(mbox_file, number):
    mbox = mailbox.mbox(mbox_file)
    messages = []
    froms = itertools.cycle(["noufal@gmail.com", "noufal@emacsmovies.org", "noufal@nibrahim.net.in"])
    tos = itertools.cycle(["user1@example.com", "user2@example.com"])


    for n in range(int(number)):
        message = create_message(froms.next(),
                                 tos.next(),
                                 generate_content("number %d"%n),
                                 {"Subject": "Test email #%d"%n})
        mbox.add(message)

    mbox.close()
    

    

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv[1], sys.argv[2]))
