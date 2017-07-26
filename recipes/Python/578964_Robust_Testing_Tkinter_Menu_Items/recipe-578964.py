# module: acc.py

import codecs
import configparser
import os
from tkinter import *
from tkinter import messagebox


class AccountWindow(Tk):
    def __init__(self):
        super().__init__()
        self.config = configparser.ConfigParser()
        head, _ = os.path.split(__file__)
        path_ = os.path.normpath(os.path.join(head, 'config.ini'))
        with codecs.open(path_, 'r', 'utf8') as f:
            self.config.read_file(f)

        self.title(self.config.get('GUI Account', 'title'))
        self.option_add('*tearOff', False)
        self.name = 'account window'

        menubar = Menu(self, name='account menubar')
        self['menu'] = menubar
        menu_help = Menu(menubar, name='help menu')
        menu_help.add_command(
            label=self.config.get('GUI Account', 'help help'),
            command=self.help_)
        menu_help.add_command(
            label=self.config.get('GUI Account', 'help about'),
            command=self.about)
        menubar.add_cascade(
            menu=menu_help,
            label=self.config.get('GUI Account', 'menu help'))

    def help_(self):
        title = self.config.get('GUI Help', 'title')
        message = self.config.get('GUI Help', 'message')
        messagebox.showinfo(title, message, icon='question', parent=self)

    def about(self):
        title = self.config.get('GUI About', 'title')
        message = self.config.get('GUI About', 'message')
        messagebox.showinfo(title, message, parent=self)


def main():
    app = AccountWindow()
    app.mainloop()

if __name__ == '__main__':
    sys.exit(main())


######################################################################
# -*- coding: utf-8 -*-
# file: config.ini

[GUI Account]
title = Accounts
menu help = Help
help help = View Help
help about = About Accounts

[GUI About]
title = About
message = About text

[GUI Help]
title = Help
message = Help text


######################################################################
# -*- coding: utf-8 -*-
# test_acc.py

import unittest
import unittest.mock

import acc


class TestAccountWindow(unittest.TestCase):
    HELP_HELP = 'Help help'
    HELP_ABOUT = 'Help about'

    def setUp(self):
        self.config = ['',  # __init__() config calls, Window title.
                       self.HELP_HELP,  # Help menu item
                       self.HELP_ABOUT,  # About menu item
                       '']  # Help menu

    def test_menu_help_item_help(self):
        self.messagebox_helper(self.HELP_HELP, icon='question')

    def test_menu_help_item_about(self):
        self.messagebox_helper(self.HELP_ABOUT)

    @unittest.mock.patch('acc.configparser.ConfigParser.get', autospec=True)
    @unittest.mock.patch('acc.messagebox.showinfo', autospec=True)
    def messagebox_helper(
            self, menu_item, mock_messagebox, mock_get_value, **kwargs):
        self.config += ['title',  # app.messagebox config calls
                        'message']
        mock_get_value.side_effect = self.config
        self.app = acc.AccountWindow()
        self.app.children['account menubar'].children['help menu'].invoke(
            menu_item)
        mock_messagebox.assert_called_with(self.config[-2],
                                           self.config[-1],
                                           parent=self.app, **kwargs)
