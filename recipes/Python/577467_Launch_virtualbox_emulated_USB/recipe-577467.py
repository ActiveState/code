#!/usr/bin/python
# -*- coding: utf-8 -*-
''' Sets sound emulation variables for USB microphone CARD_NAME. 
Also sets the microphone volume level, since that is often set at 
zero in the Linux context. VirtualBox is reniced for better
performance.'''

import codecs
from os import environ, system
from subprocess import Popen, PIPE
from time import sleep
import sys

HOME = environ['HOME']
CARD_NAME = 'C-Media USB Audio Device'

def start_vm():
    """Start the virtual machine, possible using emulation."""

    my_env = environ
    if opts.emulate:
        # aplay -l | awk '/C-Media USB Audio Device/ { print $2 }' | sed 's/:/,/'
        # VBOX_ALSA_DAC_DEV="hw:1,0" VBOX_ALSA_ADC_DEV="hw:1,0" VirtualBox -startvm "urd-xp"
        aplay_output = Popen(["aplay", "-l"], stdout=PIPE).communicate()[0].splitlines()
        for line in aplay_output:
            if CARD_NAME in line:
                card_info = line.split(' ')
                card_number = card_info[1][0:-1]
                print "card_number", card_number
                DEVICE = 'hw:%s,0' % card_number
                my_env["VBOX_ALSA_DAC_DEV"] = DEVICE
                my_env["VBOX_ALSA_ADC_DEV"] = DEVICE
                # amixer -c 1 cset name='Auto Gain Control' 0
                Popen(['amixer', '-c', card_number, 'cset', 'name=Auto Gain Control', '0']) #1
                Popen(['amixer', '-c', card_number, 'cset', 'name=Mic Capture Volume', '16']) #13
                Popen(['amixer', '-c', card_number, 'cset', 'name=Mic Playback Volume', '12'])
                Popen(['amixer', '-c', card_number, 'cset', 'name=Speaker Playback Volume', '120'])
                break
        if not card_number:
            print "\nSorry, %s not found" % CARD_NAME
            print aplay_output
            sys.exit()
            
    ## echo "$USER ALL= NOPASSWD:/usr/bin/renice,/usr/bin/nice" >> /etc/sudoers
    # VirtualBox -startvm urd-xp & sleep 4; \
    # sudo renice -n -5 `ps -eL | g VirtualBox | awk '{print $2}'`
    Popen(['VirtualBox', '-startvm', 'urd-xp'], env = my_env)
    sleep(4)
    print "** renicing"
    Popen("sudo renice -n -3 `ps -eL | grep VirtualBox | awk '{print $2}'`", 
        shell = True)

if '__main__' == __name__:
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

    import optparse # Late import, in case this project becomes a library
    opt_parser = optparse.OptionParser(usage="usage: %prog [options] FILE")
    opt_parser.add_option('-e', '--emulate', 
                    action="store_true", default=False,
                    help="Use USB sound as emulated hardware")
    opts, args = opt_parser.parse_args()

    start_vm()
