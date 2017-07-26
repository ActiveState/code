#!/usr/bin/env python                                                                                                        
# -*- coding: utf-8 -*-                                                                                                      
#                                                                                                                            
# Author: Jonathan Cervidae <jonathan.cervidae@gmail.com>                                                                    
# PGP Fingerprint: 2DC0 0A44 123E 6CC2 EB55  EAFB B780 421F BF4C 4CB4                                                        
# Last changed: $LastEdit: 2009-05-16 18:53:50 BST$                                                                          
#
# After creating this program, googling for the tag names it found located me
# this document:
#
# http://cpansearch.perl.org/src/RJRAY/Perl-RPM-1.51/RPM/Constants.pm
#
# Which nicely describes what each of these tags are for.

import rpm
import pprint

def is_a_key(string):
    for character in string:
        ordinal = ord(character)
        if ordinal is not 95 and ( ordinal < 65 or ordinal > 90 ):
            return False
        return True

header_keys = []
transaction_set = rpm.TransactionSet()
match_iterator = transaction_set.dbMatch()

# Map RPM key names to numbers
numbers_to_names = {}
for attribute_name in dir(rpm):
    if not is_a_key(attribute_name):
        continue
    if not isinstance(rpm.__dict__[attribute_name], int):
        continue
    numbers_to_names[rpm.__dict__[attribute_name]] = attribute_name

header = None
while match_iterator:
    try:
        header = match_iterator.next()
    except StopIteration:
        raise RuntimeError, "Not any headers"
    break

header_metadata = {}
for key in header.keys():
    header_metadata[numbers_to_names[key]] = header[key]

pprint.pprint(header_metadata)
