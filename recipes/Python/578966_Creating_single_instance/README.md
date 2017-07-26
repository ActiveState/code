###Creating a single instance application

Originally published: 2014-11-20 11:46:51
Last updated: 2014-11-20 11:59:46
Author: Matteo Bertini

Sometimes it is necessary to ensure that only one instance of application is running. This quite simple solution uses mutex to achieve this, and will run only on Windows platform.