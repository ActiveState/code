#!/usr/bin/env python3
#
#   Copyright (c) 2010-2011, Andrew Grigorev <andrew@ei-grad.ru>
#   All rights reserved.
#
#   Redistribution and use in source and binary forms, with or without
#   modification, are permitted provided that the following conditions are
#   met:
#
#       Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.  Redistributions
#       in binary form must reproduce the above copyright notice, this list of
#       conditions and the following disclaimer in the documentation and/or
#       other materials provided with the distribution.  Neither the name of
#       the <ORGANIZATION> nor the names of its contributors may be used to
#       endorse or promote products derived from this software without
#       specific prior written permission.
#
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#   IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#   THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#   PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
#   CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#   EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#   PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#   PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#   LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#   NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#   SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

"""
802.1X EAP-MD5 supplicant.
"""

import sys
import socket
from fcntl import ioctl
from select import select
from struct import pack, unpack
from hashlib import md5
from getpass import getpass
from optparse import OptionParser

import logging

pae_group_addr = b"\x01\x80\xc2\x00\x00\x03"
ETH_P_PAE = 0x888E # Port Access Entity (IEEE 802.1X)

def build_mreq(ifindex):
    """
    struct packet_mreq {
        int mr_ifindex;
        unsigned short int mr_type;
        unsigned short int mr_alen;
        unsigned char mr_address[8];
    };
    """
    PACKET_MR_MULTICAST = 0
    return pack('IHH8s', ifindex, PACKET_MR_MULTICAST,
            len(pae_group_addr), pae_group_addr)

def get_ifindex(sock, ifname):
    """
    IFNAMSIZ = 16

    struct ifreq {
        union {
            char ifrn_name[IFNAMSIZ];   /* Interface name, e.g. "eth0".  */
        } ifr_ifrn;

        union {
            struct sockaddr ifru_addr;
            struct sockaddr ifru_dstaddr;
            struct sockaddr ifru_broadaddr;
            struct sockaddr ifru_netmask;
            struct sockaddr ifru_hwaddr;
            short int ifru_flags;
            int ifru_ivalue;
            int ifru_mtu;
            struct ifmap ifru_map;
            char ifru_slave[IFNAMSIZ];  /* Just fits the size */
            char ifru_newname[IFNAMSIZ];
            __caddr_t ifru_data;
        } ifr_ifru;
    };
    """
    SIOCGIFINDEX = 0x8933
    ifname, ifindex = unpack('16sI',
            ioctl(sock, SIOCGIFINDEX, pack('16sI', ifname, 0)))
    return ifindex

def get_hwaddr(sock, ifname):
    """
    struct sockaddr {
        ushort  sa_family;
        char    sa_data[14];
    };
    """
    SIOCGIFHWADDR = 0x8927
    ifname, sa_family, hwaddr = unpack('16sH6s',
            ioctl(sock, SIOCGIFHWADDR, pack('16sH6s', ifname, 0, '')))
    return hwaddr

def hwaddr_to_str(hwaddr):
    return ':'.join([ "%.2x" % i for i in hwaddr])

class MD5Supplicant(object):

    def __init__(self, ifname, user_id=None, user_pw=None, interactive=False):

        self.state = 0

        self.user_id = user_id
        self.user_pw = user_pw

        self.interactive = interactive

        self.assoc_hwaddr = None

        self.ifname = ifname
        self.sock = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_PAE))
        self.sock.bind((ifname, 0))
        self.ifindex = get_ifindex(self.sock, self.ifname)
        self.hwaddr = get_hwaddr(self.sock, self.ifname)

        SOL_PACKET = 263
        PACKET_ADD_MEMBERSHIP = 1
        self.sock.setsockopt(SOL_PACKET, PACKET_ADD_MEMBERSHIP,
                build_mreq(self.ifindex))

    def get_user_id(self, identity="Identity:"):
        if self.interactive and self.user_id is None:
            self.user_id = input(identity + ' ')
        return self.user_id

    def get_user_pw(self, force=False):
        if self.interactive and self.user_pw is None:
            self.user_pw = getpass()
        return self.user_pw

    def make_ether_header(self):
        return pack('>6s6sH', pae_group_addr, self.hwaddr, ETH_P_PAE)

    def make_8021x_header(self, x_type, length=0):
        return pack('>BBH', 1, x_type, length)

    def make_eap_pkt(self, eap_code, eap_id, eap_data):
        return pack('>BBH%ds' % len(eap_data), eap_code, eap_id,
                len(eap_data) + 4, eap_data)

    def send_start(self):
        X_TYPE_START = 1
        pkt = self.make_ether_header()
        pkt += self.make_8021x_header(X_TYPE_START, 0)
        self.sock.send(pkt)
        logging.info('Start packet sent.')
        self.state = 0

    def handle(self):

        X_TYPE_EAP_PACKET = 0

        EAP_CODE_REQUEST = 1
        EAP_CODE_RESPONSE = 2
        EAP_CODE_SUCCESS = 3
        EAP_CODE_FAILURE = 4

        EAP_TYPE_IDENTITY = 1
        EAP_TYPE_MD5CHALLENGE = 4

        data = self.sock.recv(65535)
        logging.debug('Received packet of length %d.' % len(data))

        # Ethernet check
        ether_dst, ether_src, ether_type = unpack('>6s6sH', data[:14])
        if ether_dst != pae_group_addr or ether_type != ETH_P_PAE:
            logging.debug('Ethernet check failed: dst=%s type=%d' % (
                 hwaddr_to_str(ether_dst), ether_type))
            return

        if self.assoc_hwaddr is None:
            self.assoc_hwaddr = ether_src
            logging.info('Associated with %s.' % hwaddr_to_str(ether_src))
        elif self.assoc_hwaddr != ether_src:
            logging.warning('Wrong nearest device %s!' % hwaddr_to_str(ether_src))
            return

        # 802.1X check
        a_8021x_ver, a_8021x_type, a_8021x_length = unpack('>BBH', data[14:18])
        if a_8021x_ver != 1 and a_8021x_type != 0:
            logging.debug('802.1X check failed: ver=%d type=%d' % (
                a_8021x_ver, a_8021x_type))
            return

        # EAP length check
        eap_code, eap_id, eap_length = unpack('>BBH', data[18:22])
        if eap_length > len(data) - 18 or eap_length != a_8021x_length:
            logging.debug('EAP length check failed: len=%d len(802.1X)=%d' % (
                eap_length, a_8021x_length))
            return

        if self.state == 0:
            if eap_code == EAP_CODE_REQUEST and eap_length >= 5:

                eap_type = unpack('B', data[22:23])[0]

                if eap_type == EAP_TYPE_IDENTITY:
                    logging.debug('State 0 message received.')

                    if eap_length > 5:
                        identity = str(unpack('%ds' % (eap_length - 5), data[23:18+eap_length])[0], 'utf-8')
                    else:
                        identity = 'Login:'

                    pkt = self.make_ether_header()
                    user_id = self.get_user_id(identity)
                    eap_pkt = self.make_eap_pkt(EAP_CODE_RESPONSE, eap_id,
                        pack('B%ds' % len(user_id), EAP_TYPE_IDENTITY, user_id))
                    pkt += self.make_8021x_header(X_TYPE_EAP_PACKET, len(eap_pkt))
                    pkt += eap_pkt

                    self.sock.send(pkt)

                    logging.info('Identity sent.')
                    self.state = 1
            else:
                logging.debug('State 0 - EAP check failed: code=%d id=%d length=%d type=%d' % (
                    eap_code, eap_id, eap_length, unpack('B', data[22:23])[0]))
        elif self.state == 1:
            if eap_code == EAP_CODE_REQUEST and eap_length >= 5:

                eap_type = unpack('B', data[22:23])[0]

                if eap_type == EAP_TYPE_MD5CHALLENGE:
                    logging.debug('State 1 message received.')

                    eap_value_size = unpack('B', data[23:24])[0]
                    if eap_value_size != eap_length - 6:
                        logging.debug('State 1 wrong MD5 challenge value size: size=%d' % eap_value_size)
                        return

                    challenge = data[24:24+eap_value_size]

                    response = md5(bytes([eap_id]) + bytes(self.get_user_pw(), 'utf-8') + challenge).digest()

                    pkt = self.make_ether_header()
                    eap_pkt = self.make_eap_pkt(EAP_CODE_RESPONSE, eap_id,
                            pack('BB16s', EAP_TYPE_MD5CHALLENGE, 16, response))
                    pkt += self.make_8021x_header(X_TYPE_EAP_PACKET, len(eap_pkt))
                    pkt += eap_pkt

                    self.sock.send(pkt)

                    logging.info('MD5-Challenge response sent.')
                    self.state = 2
                    return
            elif eap_code == EAP_CODE_FAILURE and eap_length == 4:
                logging.info('Wrong identity.')
                if self.interactive:
                    self.user_id = None
                    self.user_pw = None
                    self.state = 0
                else:
                    raise Exception('Wrong identity, running in non-interactive mode.')
            else:
                logging.debug('State 0 - EAP check failed: code=%d id=%d length=%d type=%d' % (
                    eap_code, eap_id, eap_length, unpack('B', data[22:23])[0]))
                return

        elif self.state == 2:
            if eap_code == EAP_CODE_SUCCESS and eap_length == 4:
                logging.info('Authentication succeeded.')
                self.state = 0
            else:
                logging.info('Authentication failed!')
                if self.interactive:
                    self.user_pw = None
                    self.state = 0

    def run(self):

        self.send_start()

        while True:
            r, w, x = select([self.sock], [], [self.sock])
            if x:
                raise Exception('socket exception')
            self.handle()

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option('-i', '--iface', dest='iface', metavar='IFNAME',
            help='имя сетевого интерфейса', default='eth0')
    parser.add_option('-u', '--user', dest='user_id', metavar='LOGIN',
            help='имя пользователя')
    parser.add_option('-p', '--pass', dest='user_pw', metavar='PASSWORD',
            help='пароль')
    parser.add_option('-e', '--interactive', action='store_true', dest='interactive',
            help='интерактивный режим', default=False)
    parser.add_option('-d', '--daemonize', action='store_true', dest='daemonize',
            help='режим демона', default=False)
    parser.add_option('-l', '--logfile', dest='logfile', metavar='FILENAME',
            help='файл лога (только в режиме демона)', default='/var/log/eap-md5.log')
    parser.add_option('-G', '--debug', action='store_true', dest='debug',
            help='вывод отладочных сообщений', default=False)
    parser.add_option('-q', '--quiet', action='store_true', dest='quiet',
            help='тихий режим', default=False)
    opt, args = parser.parse_args()

    if opt.daemonize and opt.interactive:
        logging.warning('daemonize set, interactive ignored')
        opt.interactive = False

    if not opt.interactive:
        for i in (opt.user_id, opt.user_pw):
            if i is None:
                logging.error('user and pass are required in non interactive mode')
                sys.exit(1)

    if opt.quiet:
        loglevel = logging.ERROR
    elif opt.debug:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    if opt.daemonize:

        from daemon import DaemonContext
        with DaemonContext():
            logging.basicConfig(filename=opt.logfile,
                    level=loglevel,
                    format="%(asctime)s - %(levelname)s - %(funcName)s: %(message)s")

            s = MD5Supplicant(opt.iface, opt.user_id, opt.user_pw)
            s.run()

    else:

        logging.basicConfig(level=loglevel,
            format="%(asctime)s - %(levelname)s - %(funcName)s: %(message)s")

        s = MD5Supplicant(opt.iface, opt.user_id, opt.user_pw, opt.interactive)
        s.run()
