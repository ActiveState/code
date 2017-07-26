from __future__ import print_function
"""
char_to_ascii_code.py
Purpose: Show ASCII code for a given character, interactively, 
in a loop. Show trapping of KeyboardInterrupt and EOFError exceptions.
Author: Vasudev Ram
Web site: https://vasudevram.github.io
Blog: https://jugad2.blogspot.com
Product store: https://gumroad.com/vasudevram
"""

print("This program shows the ASCII code for any given ASCII character.")
print("Exit the program by pressing Ctrl-C or Ctrl-Z.")
print()

while True:
    try:
        c = raw_input( \
        "Enter an ASCII character to see its ASCII code: ")
        if len(c) != 1:
            print("Error: need a string of length 1; retry.")
            continue
        print("Character:", c)
        print("Code:", ord(c))
    except KeyboardInterrupt as ki:
        print("Caught:", repr(ki))
        print("Exiting.")
        break
    except EOFError as eofe:
        print("Caught:", repr(eofe))
        print("Exiting.")
        break
        
