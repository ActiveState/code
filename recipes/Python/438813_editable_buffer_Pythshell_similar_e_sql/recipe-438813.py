# Python Console with an editable buffer.
import os
from tempfile import mkstemp
from code import InteractiveConsole

EDITOR = os.environ.get('EDITOR', 'vim')
EDIT_CMD = '\e'

class EditableBufferInteractiveConsole(InteractiveConsole):
    def __init__(self, *args):
        self.last_buffer = [] # This holds the last executed statement
        InteractiveConsole.__init__(self, *args)

    def runsource(self, source, *args):
        self.last_buffer = [ source ]
        return InteractiveConsole.runsource(self, source, *args)

    def raw_input(self, *args):
        line = InteractiveConsole.raw_input(self, *args)
        if line == EDIT_CMD:
            fd, tmpfl = mkstemp()
            os.write(fd, '\n'.join(self.last_buffer))
            os.close(fd)
            os.system('%s %s' % (EDITOR, tmpfl))
            line = open(tmpfl).read()
            os.unlink(tmpfl)
            tmpfl = ''
        return line

c = EditableBufferInteractiveConsole()
c.write("""
Starting the editable interactive console.
Edit command is '%s'.

""" % EDIT_CMD)
c.interact(banner='')
