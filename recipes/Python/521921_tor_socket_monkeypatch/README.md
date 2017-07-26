## tor socket monkeypatch  
Originally published: 2007-06-21 01:05:41  
Last updated: 2007-06-21 08:10:06  
Author: Andrew Moffat  
  
patches socket to tunnel through a tor server either by socks4a or socks5 (tor-resolve required for socks5), being careful not to leak dns requests

pyconstruct required, http://construct.wikispaces.com/