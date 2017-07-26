#!/usr/bin/python
import binascii

def tlv(s):
  try:
    tag = s.next()
  except StopIteration:
    return {}

  if ord(tag) & 0x1f == 0x1f:
    tag += s.next()
    while ord(tag[-1]) & 0x80 == 0x80: tag += s.next()

  length = ord(s.next())
  if length & 0x80 == 0x80:
    lendata = "".join([s.next() for i in range(length & 0x7f)])
    length = int(binascii.b2a_hex(lendata), 16)

  value = "".join([s.next() for i in range(length)])
  return {binascii.b2a_hex(tag): value}

ber = (
"\x63\x04hell"                  # simple tag, len
"\x64\x04hell"                  # test read length
"\x1f\x81\x82\x82\x04\x00"      # extended tag
"\x65\x81\x01!"                 # extended len
"\x65\x83\x00\x00\x04!..!"      # mroe extended len
)
seq = (b for b in ber)
rv = dict()
while True:
  d = tlv(seq)
  if not d: break
  rv.update(d)

import pprint
pprint.pprint(rv)
