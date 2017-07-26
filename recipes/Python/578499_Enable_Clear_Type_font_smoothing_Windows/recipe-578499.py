# install pywin32 from http://sourceforge.net/projects/pywin32/files/pywin32/Build%20218/
import win32con
import win32gui
import sys

new_state = True

if len(sys.argv) > 1:
    new_state = sys.argv[1].lower() not in ['0', 'false', 'off', 'disable']

win32gui.SystemParametersInfo(win32con.SPI_SETFONTSMOOTHING, new_state, 0)
win32gui.SystemParametersInfo(win32con.SPI_SETFONTSMOOTHINGTYPE,
        win32con.FE_FONTSMOOTHINGCLEARTYPE,
        win32con.SPIF_UPDATEINIFILE | win32con.SPIF_SENDCHANGE)
