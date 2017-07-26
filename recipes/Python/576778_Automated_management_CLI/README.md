## Automated management of CLI devices  
Originally published: 2009-05-27 01:24:12  
Last updated: 2009-05-27 01:24:12  
Author: Alan Holt  
  
This recipe provides a mechanism for remote, automated control of a network device via its command-line interface (CLI). It assumes that the CLI is accessed using Telnet. Furthermore, the device cannot be accessed directly, instead the user has to SSH to an intermediate jump host before Telneting to the device. 