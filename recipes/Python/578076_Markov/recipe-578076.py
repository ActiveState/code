"""Demonstrate usage of the Markov Encryption module's features.

This program is meant to act as an example of how to use ME with
data that needs to be obfuscated. The functionality provided via
the GUI demonstrates both the ability to encrypt and decrypt all
text that the UTF-8 encoding can handle. Explanations come later."""

__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'
__date__ = '13 March 2012'
__version__ = 2, 0, 0

################################################################################

# Import functions, classes, and modules needed to create ME demo.

from tkinter import NoDefaultRoot, Tk, StringVar, BooleanVar
from tkinter.ttk import \
     Frame, LabelFrame, Radiobutton, Checkbutton, Label, Entry
from tkinter.constants import W, EW, NSEW, WORD, SEL, END, NORMAL, DISABLED
from tkinter.scrolledtext import ScrolledText

import traceback
import ast
import me

################################################################################

class MarkovDemo(Frame):

    "MarkovDemo(master=None, **kw) -> MarkovDemo instance"

    TEXT = dict(height=2, width=46, wrap=WORD)  # Text Options
    GRID = dict(padx=5, pady=5)                 # Grid Options

    # Initialize a MarkovDemo instance with a GUI for interaction.

    def __init__(self, master=None, **kw):
        "Initialize the MarkovDemo instance's widgets and settings."
        super().__init__(master, **kw)
        self.build_widgets()
        self.place_widgets()
        self.setup_widgets()
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.key = self.primer = None

    def build_widgets(self):
        "Build the various widgets that will be used in the program."
        # Create processing frame widgets.
        self.processing_frame = LabelFrame(self, text='Processing Mode:')
        self.mode_var = StringVar(self, 'encode')
        self.decode_button = Radiobutton(self.processing_frame,
                                         text='Decode Cipher-Text',
                                         command=self.handle_radiobuttons,
                                         value='decode',
                                         variable=self.mode_var)
        self.encode_button = Radiobutton(self.processing_frame,
                                         text='Encode Plain-Text',
                                         command=self.handle_radiobuttons,
                                         value='encode',
                                         variable=self.mode_var)
        self.freeze_var = BooleanVar(self, False)
        self.freeze_button = Checkbutton(self.processing_frame,
                                         text='Freeze Key & Primer',
                                         command=self.handle_checkbutton,
                                         offvalue=False,
                                         onvalue=True,
                                         variable=self.freeze_var)
        # Create encoding frame widgets.
        self.encoding_frame = LabelFrame(self, text='Encoding Options:')
        self.chain_size_label = Label(self.encoding_frame, text='Chain Size:')
        self.chain_size_entry = Entry(self.encoding_frame)
        self.plain_text_label = Label(self.encoding_frame, text='Plain-Text:')
        self.plain_text_entry = Entry(self.encoding_frame)
        # Create input frame widgets.
        self.input_frame = LabelFrame(self, text='Input Area:')
        self.input_text = ScrolledText(self.input_frame, **self.TEXT)
        # Create output frame widgets.
        self.output_frame = LabelFrame(self, text='Output Area:')
        self.output_text = ScrolledText(self.output_frame, **self.TEXT)

    def place_widgets(self):
        "Place the widgets where they belong in the MarkovDemo frame."
        # Locate processing frame widgets.
        self.processing_frame.grid(sticky=EW, **self.GRID)
        self.decode_button.grid(row=0, column=0, **self.GRID)
        self.encode_button.grid(row=0, column=1, **self.GRID)
        self.freeze_button.grid(row=0, column=2, **self.GRID)
        # Locate encoding frame widgets.
        self.encoding_frame.grid(sticky=EW, **self.GRID)
        self.chain_size_label.grid(row=0, column=0, sticky=W, **self.GRID)
        self.chain_size_entry.grid(row=0, column=1, sticky=EW, **self.GRID)
        self.plain_text_label.grid(row=1, column=0, sticky=W, **self.GRID)
        self.plain_text_entry.grid(row=1, column=1, sticky=EW, **self.GRID)
        self.encoding_frame.grid_columnconfigure(1, weight=1)
        # Locate input frame widgets.
        self.input_frame.grid(sticky=NSEW, **self.GRID)
        self.input_text.grid(sticky=NSEW, **self.GRID)
        self.input_frame.grid_rowconfigure(0, weight=1)
        self.input_frame.grid_columnconfigure(0, weight=1)
        # Locate output frame widgets.
        self.output_frame.grid(sticky=NSEW, **self.GRID)
        self.output_text.grid(sticky=NSEW, **self.GRID)
        self.output_frame.grid_rowconfigure(0, weight=1)
        self.output_frame.grid_columnconfigure(0, weight=1)

    def setup_widgets(self):
        "Setup each widget's configuration for the events they handle."
        self.input_text.bind('<Key>', self.handle_key_events)
        self.input_text.bind('<Control-Key-a>', self.handle_control_a)
        self.input_text.bind('<Control-Key-/>', lambda event: 'break')
        self.output_text['state'] = DISABLED
        self.output_text.bind('<Control-Key-a>', self.handle_control_a)
        self.output_text.bind('<Control-Key-/>', lambda event: 'break')

    ########################################################################

    # Take care of any special event needing dedicated processing.

    def handle_radiobuttons(self):
        "Change the interface based on the encoding / decoding setting."
        if self.encrypting:
            self.freeze_button.grid()
            if not self.freeze_var.get():
                self.encoding_frame.grid()
        else:
            self.freeze_button.grid_remove()
            if not self.freeze_var.get():
                self.encoding_frame.grid_remove()
        self.handle_key_events(None)

    def handle_checkbutton(self):
        "Change the interface based on the key / primer freeze setting."
        if self.freeze_var.get():
            self.encoding_frame.grid_remove()
        else:
            self.encoding_frame.grid()

    def handle_key_events(self, event):
        "Schedule refreshing the output area after an input area event."
        if event is None or event.char and event.state | 0o11 == 0o11:
            self.after_idle(self.refresh)

    @staticmethod
    def handle_control_a(event):
        "Select all text in the widget associated with the given event."
        event.widget.tag_add(SEL, 1.0, END + '-1c')
        return 'break'

    ########################################################################

    # Handle interface's updates when either encoding or decoding.

    def refresh(self):
        "Refresh the output based on the value of the input."
        text = self.input_text.get(1.0, END + '-1c')
        if not text:
            self.output = text
        elif self.encrypting:
            self.encode(text)
        else:
            self.decode(text)

    def output(self, value):
        "Set the text in the output area to the string value."
        self.output_text['state'] = NORMAL
        self.output_text.delete(1.0, END)
        self.output_text.insert(END, value)
        if self.encrypting and self.freeze_var.get():
            self.output_text.see(END)
        self.output_text['state'] = DISABLED

    output = property(fset=output, doc='Output area property.')

    @property
    def chain_size(self):
        "Chain size for the Markov chains used when encrypting."
        try:
            value = ast.literal_eval(self.chain_size_entry.get())
            assert isinstance(value, int) and 2 <= value <= 256
            return value
        except:
            self.chain_size_entry.delete(0, END)
            self.chain_size_entry.insert(0, '2')
            return 2

    @property
    def plain_text(self):
        "Plain text or ignored characters in encryption process."
        try:
            value = self.repr_to_obj(self.plain_text_entry.get(), '')
            assert isinstance(value, str)
            return value
        except:
            self.plain_text_entry.delete(0, END)
            return ''

    ########################################################################

    # Encrypt a string for display in the interface's output area.

    def encode(self, string):
        "Encode the string and show the cipher-text in the output."
        try:
            cipher = self.build_cipher(string)
        except ValueError:
            self.output = ''
        except:
            self.output = traceback.format_exc()
        else:
            self.output = self.build_header() + '\n\n' + cipher

    def build_cipher(self, string):
        "Build cipher-text based on plain-text and return answer."
        if self.key and self.freeze_var.get():
            cipher, primer = me.encrypt_str(string, self.key, self.primer)
        else:
            args = string, self.chain_size, self.plain_text
            cipher, self.key, self.primer = me.auto_encrypt_str(*args)
        return cipher

    def build_header(self):
        "Build header from key and primer values in current use."
        header = '\n'.join(map(self.bytes_to_repr, self.key.data))
        header += '\n' + self.bytes_to_repr(self.primer.data)
        return header

    ########################################################################

    # Decrypt a string for display in the interface's output area.

    def decode(self, string):
        "Decode encrypted message and display plain-text in output."
        try:
            cipher = self.extract_keys(string)
            text = self.extract_text(cipher)
        except ValueError:
            self.output = ''
        except:
            self.output = traceback.format_exc()
        else:
            self.output = text

    def extract_keys(self, string):
        "Extract keys to decryption and return the cipher-text area."
        header, cipher = string.split('\n\n', 1)
        *key, primer = map(self.repr_to_obj, header.split('\n'))
        self.key, self.primer = me.Key(tuple(key)), me.Primer(primer)
        return cipher

    def extract_text(self, string):
        "Extract text message from string using built key and primer."
        text, primer = me.decrypt_str(string, self.key, self.primer)
        return text

    ########################################################################

    # Provide some special methods to simplify the program's code.

    @property
    def encrypting(self):
        "Encrypting boolean stating current operations mode."
        return {'encode': True, 'decode': False}[self.mode_var.get()]

    @staticmethod
    def bytes_to_repr(obj):
        "Convert bytes object into suitable representation."
        if not isinstance(obj, bytes):
            raise TypeError('Object must be a bytes instance!')
        return repr(obj)[2:-1]

    @staticmethod
    def repr_to_obj(string, prefix='b'):
        "Convert representation into an equivalent object."
        for template in '{}"{}"', "{}'{}'":
            try:
                return ast.literal_eval(template.format(prefix, string))
            except:
                pass
        raise ValueError('Cannot convert {!r} to object!'.format(string))

    @classmethod
    def main(cls):
        "Create context for demo and run a test instance."
        NoDefaultRoot()
        root = Tk()
        root.minsize(420, 330)
        root.title('Markov Demo 2')
        test = cls(root)
        test.grid(sticky=NSEW)
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.mainloop()

################################################################################

# Start the demonstration if this module was run and not imported.

if __name__ == '__main__':
    MarkovDemo.main()
