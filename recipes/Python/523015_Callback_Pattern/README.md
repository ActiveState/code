## Callback Pattern

Originally published: 2007-07-03 12:03:45
Last updated: 2007-07-03 12:03:45
Author: Javier Burroni

when adding callbacks, the code may not be very focused on the actual problem.\nA solution si to write a generic base class to deal with the callbacks issues, and then decorate the methods with the event for wich you want a binding.