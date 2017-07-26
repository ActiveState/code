#!/usr/bin/env python -E

print "Nope, this doesn't work"



#!/bin/sh
LOADER=''''; exec python -E "$0" "$@" #'''

print "This Python script is also a shell script!"
