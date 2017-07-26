## csc prototype to arduino board with python API. part I  
Originally published: 2010-12-26 11:51:30  
Last updated: 2010-12-26 12:14:33  
Author: cheeng shu chin  
  
Few day ago, i'm try out arduino UNO robotic board. found it not that easy to use (C <--> Python).
I wrote a arduino UNO prototype to serial API, which can interface to any programming Language.
as long as the programming Language can interface to virtual serial port and using serial API, this recipe can be use...
Requirement:

  Upload this recipes to arduino uno with my prototype code (name "csc.pde" as below)

Base concept:

  1. wait from serial reply "?" and ready for read
  2. pass function name as string to arduino uno
  3. pass all argument as string to arduino uno
  4. read result as string from arduino uno

Can easy extend it to support:

  1. python API(open source and i like most) in part II
  2. other arduino board
  3. Bluetooth with serial interface
  4. any PC can control the arduino board easily via your prefer Language.
  5. interrupt 

Future add-on:

  1. Json string passing to arduino
  2. Json Reply from arduino
  3. thread base design
  4. Interrupt direct call

Please study it and extend it and share among open source members especially in python... :)

Next [Part II](http://code.activestate.com/recipes/577521-csc-prototype-to-arduino-board-with-python-api-par/)