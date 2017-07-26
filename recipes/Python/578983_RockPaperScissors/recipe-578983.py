#!/usr/bin/env python
# -*-coding:utf-8-*-
import time
from time import sleep
import random

sus="-"*35
depo=["rock","paper","scissors"]
while True:
    x=input("rock , paper, scissors: ")
    if x not in depo:
        print ("Dont cheat!")
        continue

    pc=random.choice(depo)
    sleep(0.5)
    print (("Computer picked {}.").format(pc))
    if x==pc:
        sleep(0.5)
        print (("\nIt's a draw.\n{}").format(sus))
    elif x=="rock" and pc=="scissors":
        sleep(0.5)
        print (("\nYou win.rock beats scissors\n{}").format(sus))
    elif x=="paper" and pc=="rock":
        sleep(0.5)
        print (("\nYou win.paper beats rock\n{}").format(sus))
    elif x=="scissors" and pc=="paper":
        sleep(0.5)
        print (("\nYou win.scissors beats paper\n{}").format(sus))
    else:
        sleep(0.5)
        print (("\nYou lose. {} beats {}\n{}").format(pc,x,sus))
input()
