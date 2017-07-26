import Tkinter
import tkMessageBox
import traceback
import winreg

################################################################################

def main(key):
    'Delete key and all empty parent keys.'
    Tkinter.Tk().withdraw()
    try:
        key, parent = delete(*key.rsplit('\\', 1))
        while empty(parent):
            key, parent = delete(*key.rsplit('\\', 1))
        tkMessageBox.showinfo('Info', 'Uninstall passed!')
    except:
        tkMessageBox.showerror('Error', traceback.format_exc())

def delete(key, subkey):
    'Delete key and all subkeys.'
    parent = winreg.Key(winreg.HKEY.CURRENT_USER, key)
    del parent.keys[subkey].keys
    del parent.keys[subkey]
    return key, parent

def empty(key):
    'Test for lack of values.'
    if key.values:
        return False
    for name in key.keys:
        if not empty(key.keys[name]):
            return False
    return True

################################################################################

if __name__ == '__main__':
    main('Software\\Atlantis Zero\\Kaos Rain\\Version 3')
