PyShellHere.bat:
cd %1
python


Registry edit:
You need to add a new key in 'My Computer\HKEY_CLASSES_ROOT\Folder\shell' named 'Python Shell Here', and under that a key named 'command' with a REG_SZ value that points to your batch file and follows it with a reference to the %L variable. On my machine, this full value looks like this: "c:\utils\PyShellHere.cmd" "%L" (all quotes included).
