#!python
# -*- coding: iso-8859-1 -*-

import datetime

import py

from ll.xist import xsc
from ll.xist.ns import xml, html, meta


codetemplate = """
import os
base = %r
crontabs = os.listdir(base)
channel.send(len(crontabs))
for file in crontabs:
    channel.send((file, os.popen('crontab -u %%s -l' %% file).read()))
"""


class Host(object):
    def __init__(self, name, dir="/var/spool/cron/crontabs", python="python2.4"):
        self.name = name
        self.dir = dir
        self.python = python

    def getcrontabs(self):
        code = py.code.Source(codetemplate % self.dir)
        gateway = py.execnet.SshGateway("root@%s" % self.name, remotepython=self.python)
        channel = gateway.remote_exec(code)
        count = channel.receive()
        for i in xrange(count):
            yield channel.receive()
        gateway.exit()


hosts = [
    Host("host1.example.com"),
    Host("host2.example.org"),
    Host("host3.example.net"),
]


style = """
body {
    margin: 0;
    padding: 0;
    background-color: #fff;
    color: #000;
}

.note
{
    font-size: 13px;
}
h1, h2, h3
{
    color: #0063a8;
    font-family: "Trebuchet MS", sans-serif;
    font-weight: normal;
}

h1
{
    font-size: 30px;
    color: #fff;
    background-color: #0063a8;
    padding: 8px 30px;
}

h2
{
    font-size: 20px;
    margin: 30px 30px -10px 30px;
}

h3
{
    font-size: 14px;
    margin: 20px 30px 2px 30px;
}

pre
{
    margin: 0px 30px 10px 30px;
    font-size: 11px;
    line-height: 18px;
    border: 1px solid #eee;
    background-color: #fafafa;
    padding: 1px 5px 2px 5px;
    overflow: auto;
}
"""

now = datetime.datetime.now()

node = xsc.Frag(html.h1("Cronjobs ", html.span("(generated at %s)" % now.strftime("%d.%m.%Y %H:%M"), class_="note")))

for host in hosts:
    node.append(html.h2(host.name))
    for (user, crontab) in sorted(host.getcrontabs()):
        node.append(html.h3(user, "@", host.name))
        node.append(html.pre(crontab.decode("latin-1").strip()))

node = xsc.Frag(
    xml.XML10(), "\n",
    html.head(
        meta.contenttype(),
        html.title("Cronjobs"),
        html.style(style, type="text/css"),
    ),
    html.body(node)
)

print e.asBytes(encoding="iso-8859-1")
