## SPOJ backup script  
Originally published: 2010-02-09 08:07:14  
Last updated: 2010-02-09 08:50:44  
Author: Shashwat Anand  
  
Introduction
============
At Sphere Online Judge (http://www.spoj.pl) you are given the capability of trying out the
challenging problems given. It also gives you the capability of viewing
and downloading your own solution.

The tool spojbackup tends to automatically backup all your Accepted
submissions and save them on the desired location of your computer. The
basic idea is to automate the process which can be used as a backup and
an offline reference tool of your own codes.

Features
========

* Resume downloads.
    spojbackup currently supports resuming of the solutions if internet
    connection is disrupted

* Incremental backup facility
    it'll not download the code already present on your machine. Only newer
    code added in your signedlist will be downloaded

* User-defined destination
    all codes are saved at user-defined destination
    if no option is given by user it saves in the folder from where command is
    run

* Proxy support
    Proxy support is provided as SPOJ users are generally university students
    and they are generally behind a proxy and university firewall.

Bugs
====

In case of finding a bug please drop a mail to the authors. We will try to sort
out the problems.