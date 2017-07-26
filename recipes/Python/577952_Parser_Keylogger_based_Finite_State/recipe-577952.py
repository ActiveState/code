#!/usr/bin/python
# -*- coding: utf-8 -*-


import re, sys
import optparse
from subprocess import *

"""
This program parses the logfile given by the execution of the keylogger 
command 'script -c "xinput test ID_CODE" | cat LOG_FILE' and
it is based on a Finite State Machine (FSM) to manage all 
the possible combinations of the modifiers that represent the state of the FSM.
The parser gets the mapping between the couple of keycode and modifier typed 
and the corresponding char by xmodmap command. The parser is able to manage also extended 
combinations such as Control or Super that don't give a real char.
To introduce new possible states that represent new combinations between modifiers,
it's just necessary to update the list of state (mod_keys) and add new rules in the transition function properly.
For example to introduce the Caps Lock state just add it in mod_keys and the data structure transition has to handle 
the release event of the corresponding key.
For the dependency of xmodmap the parser works only in X11 based systems.

@author Filippo Squillace
@date 20/09/2011
@version 0.9.1
"""

# List of of the modifiers that represent also all the states of the FSM (Finite State Machine)
mod_keys = ['NORMAL', 'SHIFT_L', 'SHIFT_R', 'ISO_LEVEL3_SHIFT', 'SHIFT_R_ALT_R', 'SHIFT_L_ALT_R']
# Extended modifiers Keys don't give a concrete char in xmodmap command but only combinations of keys. 
ext_mod_keys = ['CONTROL_L', 'CONTROL_R', 'ALT_L', 'SUPER_L']
# List of keys that will be excluded by the parser
special_keys = ["UP", "DOWN", "LEFT", "RIGHT", "BACKSPACE", "TAB", "HOME", "END", "DELETE"]

# Maps the kewords appear in xmodmap -pke command into the corresponding char
transform = {}
transform['RETURN'] = '\n'
transform['SPACE'] = ' '
transform['PLUS'] = '+'
transform['MINUS'] = '-'
transform['COMMA'] = ','
transform['UNDERSCORE'] = '_'
transform['PERIOD'] = '.'
transform['COLON'] = ':'
transform['SEMICOLON'] = ';'
transform['DOLLAR'] = '$'
transform['STERLING'] = '£'
transform['QUOTEDBL'] = '"'
transform['EXCLAM'] = '!'
transform['SLASH'] = '/'
transform['BRACKETLEFT'] = '['
transform['BRACKETRIGHT'] = ']'
transform['AT'] = '@'
transform['EUROSIGN'] = '€'
transform['NUMBERSIGN'] = '#'
transform['BRACELEFT'] = '{'
transform['BRACERIGHT'] = '}'
transform['EGRAVE'] = 'è'
transform['OGRAVE'] = 'ò'
transform['AGRAVE'] = 'à'
transform['UGRAVE'] = 'ù'
transform['IGRAVE'] = 'ì'
transform['EACUTE'] = 'é'
transform['CCEDILLA'] = 'ç'
transform['DEGREE'] = '°'
transform['SECTION'] = '§'
transform['APOSTROPHE'] = '\''
transform['ASCIICIRCUM'] = '^'
transform['QUESTION'] = '?'
transform['PERCENT'] = '%'
transform['AMPERSAND'] = '&'
transform['PARENLEFT'] = '('
transform['PARENRIGHT'] = ')'
transform['EQUAL'] = '='
transform['BAR'] = '|'
transform['BACKSLASH'] = '\\'
transform['ASTERISK'] = '*'
transform['MULTIPLY'] = '×'
transform['DIVISION'] = '÷'
transform['QUESTIONDOWN'] = '¿'
transform['EXCLAMDOWN'] = '¡'
transform['PLUSMINUS'] = '±'
transform['TRADEMARK'] = '™'
transform['SEVENEIGHTHS'] = '⅞'
transform['FIVEEIGHTHS'] = '⅝'
transform['THREEEIGHTHS'] = '⅜'
transform['ONEEIGHTH'] = '⅛'
transform['ASCIITILDE'] = '~'
transform['ONESUPERIOR'] = '¹'
transform['TWOSUPERIOR'] = '²'
transform['THREESUPERIOR'] = '³'
transform['ONEQUARTER'] = '¼'
transform['ONEHALF'] = '½'
transform['NOTSIGN'] = '¬'
transform['GRAVE'] = '`'
transform['BROKENBAR'] = '¦'
transform['PARAGRAPH'] = '¶'
transform['COPYRIGHT'] = '©'
transform['REGISTERED'] = '®'
transform['NOSYMBOL'] = None



def get_key_map():
    """
    Returns the corrisponding Key based on the current status (modifier) and the keycode of the key typed.
         char = f(keycode, modifier)
    Where char is the corresponding character given by the combination.
    """
    table = Popen("xmodmap -pke", shell=True, bufsize=1, stdout=PIPE).stdout
    key_map = {}
    for line in table:
        m = re.match('keycode +(\d+) = (.+)', line.decode())
        if m:
            l = m.groups()[1].split()
            # Wipes out all the useless elements that appears in xmodmap
            nl = []
            for i in range(len(l)):
                if i==0: #NORMAL
                    nl.append(l[i])
                if i==1: #SHIFT_L
                    nl.append(l[i])
                if i==3: #SHIFT_R
                    nl.append(l[i])
                if i==4: # ISO_LEVEL3_SHIFT
                    nl.append(l[i])
                if i==5: # SHIFT_?_ALT_R
                    nl.append(l[i])
                    nl.append(l[i])

            seq = [transform.get(letter.upper(), letter) for letter in nl]
            # Add None element for the rest of the table
            seq.extend([None for i in range(len(mod_keys)-len(seq))])
            # Pad out with the remained extended combinations
            seq.extend([mod+'+'+str(seq[0]) for mod in ext_mod_keys])
            
            assert len(seq)==len(mod_keys)+len(ext_mod_keys), \
                   "Err:"+str(seq)+" has not the same size of "+str(mod_keys)+str(ext_mod_keys)
            
            key_map[m.groups()[0]] = {}
            for mod, s in zip(mod_keys+ext_mod_keys, seq):
                key_map[m.groups()[0]][mod] = s
            
    return key_map

def get_trans_func():
    """
    Returns the next status (modifier) based on the current status, 
    the event on the new modifier (pressed or released) and the new modifier typed.
         next_status = f(event, modifier, curr_status)
    event can be {'press', release}; modifier is one of the possible modifier in mod_keys 
    list and curr_status is the current modifier.
    """
    trans = {'press':{}, 'release':{}}
    for mk in mod_keys+ext_mod_keys:
        trans['press'][mk] = {}
        trans['release'][mk] = {}
        
    for mk1 in mod_keys+ext_mod_keys:
        for mk2 in mod_keys+ext_mod_keys:
            trans['press'][mk1][mk2] = 'NORMAL'
            trans['release'][mk1][mk2] = 'NORMAL'
    
    trans['press']['SHIFT_L']['NORMAL'] = 'SHIFT_L'
    trans['press']['SHIFT_R']['NORMAL'] = 'SHIFT_R'
    trans['press']['ISO_LEVEL3_SHIFT']['NORMAL'] = 'ISO_LEVEL3_SHIFT'
    trans['press']['SHIFT_R_ALT_R']['NORMAL'] = 'SHIFT_R_ALT_R'
    trans['press']['SHIFT_L_ALT_R']['NORMAL'] = 'SHIFT_L_ALT_R'
    trans['press']['CONTROL_L']['NORMAL'] = 'CONTROL_L'
    trans['press']['CONTROL_R']['NORMAL'] = 'CONTROL_R'
    trans['press']['ISO_LEVEL3_SHIFT']['NORMAL'] = 'ISO_LEVEL3_SHIFT'
    trans['press']['ALT_L']['NORMAL'] = 'ALT_L'
    trans['press']['SUPER_L']['NORMAL'] = 'SUPER_L'
    
    trans['release']['SHIFT_L']['SHIFT_L'] = 'NORMAL'
    trans['release']['SHIFT_R']['SHIFT_R'] = 'NORMAL'
    trans['release']['ISO_LEVEL3_SHIFT']['ISO_LEVEL3_SHIFT'] = 'NORMAL'
    trans['release']['SHIFT_R_ALT_R']['SHIFT_R_ALT_R'] = 'NORMAL'
    trans['release']['SHIFT_L_ALT_R']['SHIFT_L_ALT_R'] = 'NORMAL'
    trans['release']['CONTROL_L']['CONTROL_L'] = 'NORMAL'
    trans['release']['CONTROL_R']['CONTROL_R'] = 'NORMAL'
    trans['release']['ISO_LEVEL3_SHIFT']['ISO_LEVEL3_SHIFT'] = 'NORMAL'
    trans['release']['ALT_L']['ALT_L'] = 'NORMAL'
    trans['release']['SUPER_L']['SUPER_L'] = 'NORMAL'    
    

    trans['press']['SHIFT_L']['ISO_LEVEL3_SHIFT'] = 'SHIFT_L_ALT_R'
    trans['press']['ISO_LEVEL3_SHIFT']['SHIFT_L'] = 'SHIFT_L_ALT_R'
    trans['press']['SHIFT_R']['ISO_LEVEL3_SHIFT'] = 'SHIFT_R_ALT_R'
    trans['press']['ISO_LEVEL3_SHIFT']['SHIFT_R'] = 'SHIFT_R_ALT_R'
    
    trans['release']['ISO_LEVEL3_SHIFT']['SHIFT_L_ALT_R'] = 'SHIFT_L'
    trans['release']['SHIFT_L']['SHIFT_L_ALT_R'] = 'ISO_LEVEL3_SHIFT'
    trans['release']['ISO_LEVEL3_SHIFT']['SHIFT_R_ALT_R'] = 'SHIFT_R'
    trans['release']['SHIFT_R']['SHIFT_R_ALT_R'] = 'ISO_LEVEL3_SHIFT'

    return trans


if __name__ == '__main__':


    usage = "%prog [options] LOG_FILE\n" + \
          "Parse the output given by the keylogger command 'script -c \"xinput test ID_CODE\" | cat LOG_FILE'.\n"+\
          "The ID_CODE is the ID keyboard that can be got typing \"xinput list\"."
    
    parser = optparse.OptionParser(usage=usage)
    
    parser.add_option("-s","--special-chars",\
            default=False, action="store_true", dest="special_chars",\
            help="Enables the special chars (i.e. HOME, DELETE, END, LEFT, DOWN, ...)")    
    parser.add_option("-e","--extended-combinations",\
            default=False, action="store_true", dest="extended_combinations",\
            help="Enables the extended combination (i.e. CONTROL, SUPER, ...)")
    
    options, args = parser.parse_args() # by default it takes sys.argv[1:]

    
    key_map=get_key_map()
    transition = get_trans_func()
    
    f = open(args[0])
    lines = f.readlines()
    f.close()
    status = 'NORMAL'
    for line in lines:
        m = re.match('key ([a-z]+) +(\d+)', line)
        if m:
            event = m.groups()[0]
            keycode = m.groups()[1]
            try:
                ch = key_map[keycode][status]
            except IndexError:
                continue
            
            first_ch = key_map[keycode]['NORMAL'].upper()
            
            if first_ch in mod_keys+ext_mod_keys: # Change status
                status = transition[event][first_ch][status]
                
            elif ch is not None and event == 'press': # Printing char
                if not options.extended_combinations and status in ext_mod_keys: # ignore the ext combination
                    continue
                elif not options.special_chars and ch.upper() in special_keys: # ignore the special char
                    continue
                else:
                    sys.stdout.write(ch)
                
                
                
