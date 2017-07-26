## argdeclare: declarative interface to argparse  
Originally published: 2009-10-26 14:35:21  
Last updated: 2010-03-02 00:05:40  
Author: Shakeeb Alireza  
  
This is an implementation of the interface provided by the [cmdln](http://code.google.com/p/cmdln/) module but using [argparse](http://code.google.com/p/argparse/) to provide the option/arg heavy parsing.

An example of usage is provided in the `test` function, which should produce the following from the command line:

$ python argdeclare.py --help

    usage: argdeclare.py [-h] [-v] {uninstall,install,delete} ...

    a description of the test app

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit

    subcommands:
      valid subcommands

      {uninstall,install,delete}
                            additional help
        delete              help text for delete subcmd
        install             help text for install subcmd
        uninstall           help text for uninstall subcmd

$ python argdeclare.py install --help

    usage: argdeclare.py install [-h] [-t TYPE] [--log] [-f] package

    positional arguments:
      package               package to be (un)installed

    optional arguments:
      -h, --help            show this help message and exit
      -t TYPE, --type TYPE  specify type of package
      --log, -l             log is on
      -f, --force           force through installation

enjoy!


SA