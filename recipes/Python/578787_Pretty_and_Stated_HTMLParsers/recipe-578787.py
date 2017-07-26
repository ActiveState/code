"""Module for parsing HTML pages."""

# htmlpars.py by Ádám Szieberth (2013)
# Python 3.3

# Full license text:
# --------------------------------------------------------------
# DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
# Version 2, December 2004
#
# Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>
#
# Everyone is permitted to copy and distribute verbatim or
# modified copiesof this license document, and changing it is
# allowed as long as the name is changed.
#
# DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
# TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND
# MODIFICATION
#
# 0. You just DO WHAT THE FUCK YOU WANT TO.
# --------------------------------------------------------------

from functools import partial, wraps
from html.parser import HTMLParser

MAIN_HANDLERS = {"handle_startendtag", "handle_starttag",
    "handle_endtag", "handle_comment", "handle_decl",
    "handle_pi"}

class PrettyHTMLParser(HTMLParser):
    """
    This parser do not split up data in arbitrary chunks like
    html.parser.HTMLParser, so you can more easily handle them.
    Note that data is not handled by facing but immediately
    before handling the following non-data part of the page.
    Note that handle_charref() and handle_entityref() are
    depreciated in PrettyHTMLParser. Do not override them!
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._reset_data()


    def __getattribute__(self, name):
        if name == "handle_data":
            return super().__getattribute__("_handle_data")
        elif name in MAIN_HANDLERS:
            return self._handler(name)
        else:
            return super().__getattribute__(name)


    def _handle_data(self, data):
        if self._data_cont:
            self._data_buf.append(data)
            self._data_cont = False
        else:
            self._data_buf = [data]


    def _handler(self, name):
        sup = super()
        def wrapper(*args, **kwargs):
            if self._data_buf:
                # Note: Calling super() here would result
                # "SystemError: super(): no arguments"
                # exception.
                h_data = sup.__getattribute__("handle_data")
                h_data("".join(self._data_buf))
                self._reset_data()
            return sup.__getattribute__(name)(*args, **kwargs)
        return wrapper


    def _reset_data(self):
        """
        Resets the data buffer and the data continous flag.
        """
        self._data_buf, self._data_cont = [], False


    def handle_charref(self, name):
        """
        Do not ovveride this method!
        """
        data = self.unescape("&#{};".format(name))
        self._data_buf.append(data)
        self._data_cont = True


    def handle_entityref(self, name):
        """
        Do not ovveride this method!
        """
        data = self.unescape("&{};".format(name))
        self._data_buf.append(data)
        self._data_cont = True

class StatedHTMLParser(PrettyHTMLParser):
    """
    This HTML parser parent class uses a state variable to make
    user able to do a more sophisticated parsing of HTML pages.

    I suggest setting initial state and other instance variables
    in __init__() method of the subclass.

    Individual handlers should manage self.state. Handlers in
    subclasses should be named keeping the following rule:
        handle_<self_state>_<handler_type>
    For example if self.state == "goals", then to handle data,
    self.handle_goals_data() is called, to handle a startag,
    self.handle_goals_starttag() is called, etc. When the
    handler not exists, self.common_handler() is called.
    """
    def __init__(self, *args, **kwargs):
        self.state = ""
        super().__init__(*args, **kwargs)


    def common_handler(self, name, *args, **kwargs):
        pass


    def _stated_handler(self, name):
        h, n = name.split("_", 1)
        handler = "_".join((h, self.state, n))
        try:
            return super().__getattribute__(handler)
        except AttributeError:
            return partial(self.common_handler, handler)


    def _handler(self, name):
        def wrapper(*args, **kwargs):
            if self._data_buf:
                h_data = self._stated_handler("handle_data")
                h_data("".join(self._data_buf))
                self._reset_data()
            return self._stated_handler(name)(*args, **kwargs)
        return wrapper


def skips_empty_data(method):
    """
    Decorator which allows data handlers to skip empty data.
    """
    @wraps(method)
    def wrapper(parser_instance, data):
        if data.strip():
            return method(parser_instance, data)
    return wrapper
