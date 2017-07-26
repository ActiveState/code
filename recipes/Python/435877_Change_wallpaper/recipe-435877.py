import ctypes

SPI_SETDESKWALLPAPER = 20 # According to http://support.microsoft.com/default.aspx?scid=97142

ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, "myimage.jpg" , 0)
