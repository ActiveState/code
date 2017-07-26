## Quick implementation of DIP (Dynamic IP) protocol using Twisted  
Originally published: 2004-07-22 02:27:24  
Last updated: 2004-07-26 11:25:23  
Author: Nicola Paolucci  
  
Command line prototype to update a Dynamic DNS Service that
accepts the GnuDIP protocol (like yi.org):

pydyp.py [-u uname] -w password [-s dipserver] [-p dipserverport] [-d domain]

It shows the power of Twisted framework.