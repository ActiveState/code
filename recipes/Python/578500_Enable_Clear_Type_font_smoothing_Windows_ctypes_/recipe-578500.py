import sys
import os
from ctypes import windll

user32 = windll.user32

SPI_SETFONTSMOOTHING      = 0x004B # dec 75
SPI_SETFONTSMOOTHINGTYPE  = 0x200B  # dec 8203
SPIF_UPDATEINIFILE        = 0x1
SPIF_SENDCHANGE           = 0x2
FE_FONTSMOOTHINGCLEARTYPE = 0x2

is_font_smoothing_enabled = 1

if len(sys.argv) > 1:
    if sys.argv[1].lower() not in ['1', 'true', 'on', 'enable']:
        is_font_smoothing_enabled = 0

user32.SystemParametersInfoA(SPI_SETFONTSMOOTHING, is_font_smoothing_enabled, 0,
         SPIF_UPDATEINIFILE | SPIF_SENDCHANGE)
