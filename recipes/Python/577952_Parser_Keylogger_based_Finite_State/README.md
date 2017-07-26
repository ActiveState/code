## Parser Keylogger based on a Finite State Machine  
Originally published: 2011-11-20 23:22:44  
Last updated: 2011-11-21 14:53:52  
Author: Filippo Squillace  
  
This program parses the logfile given by the execution of the keylogger 
command **'script -c "xinput test ID_CODE" | cat LOG_FILE'** and
it is based on a Finite State Machine (FSM) to manage all 
the possible combinations of the modifiers that represent the state of the FSM.
The parser gets the mapping between the couple of keycode and modifier typed 
and the corresponding char by xmodmap command. The parser is able to manage also extended 
combinations such as Control or Super that don't give a real char.
To introduce new possible states that represent new combinations between modifiers,
it's just necessary to update the list of state (*mod_keys*) and add new rules in the transition function properly.
For example to introduce the Caps Lock state just add it in mod_keys and the data structure transition has to handle 
the release event of the corresponding key.
For the dependency of xmodmap the parser works only in X11 based systems.