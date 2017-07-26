import Tkinter
import tkMessageBox
import traceback
import winreg

################################################################################

CLR = {'MENU_BG': 'black',                          # MENU BACKGROUND
       'BT_NORM': 'blue',                           # NORMAL BUTTON
       'BT_HIGH': 'red',                            # HIGHLIGHTED BUTTON
       'HS_TEXT': 'green',                          # HIGH SCORE TEXT
       'GAME_BG': 'white',                          # GAME BACKGROUND
       'FLOOR': 'blue',                             # GAME FLOOR
       'FORCE': 'light green',                      # FORCE FIELDS
       'MS_TEXT': 'red',                            # WIN MESSAGE
       'CYCLE': ['#FF0000',                         # BALL COLORS
                 '#FF7F00',
                 '#FFFF00',
                 '#00FF00',
                 '#0000FF',
                 '#FF00FF']}

FNT = {'BT_NORM': 'Helvetica 25',                   # NORMAL BUTTON
       'BT_HIGH': 'Helvetica 26',                   # HIGHLIGHTED BUTTON
       'HS_TEXT': 'Courier 15',                     # HIGH SCORE TEXT
       'MS_TEXT': 'Helvetica 45'}                   # WIN MESSAGE

STR = {'GM_NAME': 'Kaos Rain (MKv3)',               # PROGRAM NAME
       'PLAY_BT': 'Start Session',                  # START BUTTON
       'MS_TEXT': 'YOU WIN !!!',                    # WIN MESSAGE
       'T_SPACE': '.',                              # TABLE SPACER
       'LOSE_TI': 'THE END',                        # LOSE TITLE
       'LOSE_MS': 'Ready for another challenge?',   # LOSE MESSAGE
       'DEFAULT': 'No Name',                        # DEFAULT NAME
       'VICT_TI': 'High Score',                     # VICTORY TITLE
       'VICT_MS': ['Please enter your name',        # VICTORY MESSAGE
                   'for the high score table.']}

PHY = {'S_LIMIT': 750,                              # SPEED LIMIT
       'W_FORCE': 2000,                             # WALL FORCE
       'G_FORCE': 200,                              # GRAVITY FORCE
       'F_FORCE': 50,                               # FRICTION FORCE
       'B_BONUS': 10}                               # BOUNCE BONUS

MNU = {'SCR_W': 500,                                # SCREEN WIDTH
       'SCR_H': 500,                                # SCREEN HEIGHT
       'N_LEN': 20,                                 # MAX NAME LENGTH
       'HST_W': 30,                                 # TABLE WIDTH
       'HST_H': 10,                                 # TABLE HEIGHT
       'START': 77}                                 # BUTTON OFFSET

GAM = {'B_ALL': 20,                                 # NUMBER OF BALLS
       'B_RAD': 15,                                 # BALL RADIUS
       'B_OFF': 100,                                # BALL OFFSET
       'W_OFF': 35,                                 # WALL OFFSET
       'F_OFF': 25,                                 # FLOOR OFFSET
       'SCR_W': 450,                                # SCREEN WIDTH
       'SCR_H': 450}                                # SCREEN HEIGHT

TMR = {'P_FPS': 60,                                 # PHYSICS FRAME RATE
       'S_FPS': 30,                                 # SCREEN FRAME RATE
       'LIMIT': 600,                                # TIME LIMIT
       'MS_FF': 500,                                # WIN FLIP FLOP
       'DELAY': 2250}                               # WIN HST DELAY

################################################################################

HST = {540: ['Wiz-Kid'],
       480: ['Speed Daemon'],
       420: ['[SW] O B 1'],
       360: ['1337 Spartan'],
       300: ['<<SHIFTED>>'],
       240: ['NovaSuperNova'],
       180: ['[ZT] Berserk Fury'],
       120: ['[ZT] Shadow'],
       60: ['newbie123'],
       0: ['SiriuS']}

################################################################################

def main(key):
    'Install previous settings.'
    Tkinter.Tk().withdraw()
    try:
        root = get_key(winreg.HKEY.CURRENT_USER, key, winreg.KEY.ALL_ACCESS)
        GLOBAL = globals()
        for name in GLOBAL.keys():
            if name.isupper():
                database = GLOBAL[name]
                name = get_key(root, name, winreg.KEY.ALL_ACCESS)
                for key in database.keys():
                    name.values[str(key)] = solve(database[key])
        tkMessageBox.showinfo('Info', 'Install passed!')
    except:
        tkMessageBox.showerror('Error', traceback.format_exc())

def get_key(key, subkey, mode=None):
    'Return the specified subkey.'
    key = winreg.Key(key)
    for subkey in subkey.split('\\'):
        if subkey not in key.keys:
            key.keys = subkey
        key = key.keys[subkey]
    return winreg.Key(key, mode=mode)

def solve(value):
    'Correctly package the value.'
    if isinstance(value, str):
        return winreg.REG_SZ(value)
    elif isinstance(value, int):
        return winreg.REG_DWORD(value)
    elif isinstance(value, list):
        return winreg.REG_MULTI_SZ(value)
    raise NotImplementedError, 'Cannot solve for %s' % type(value)

################################################################################

if __name__ == '__main__':
    main('Software\\Atlantis Zero\\Kaos Rain\\Version 3')
