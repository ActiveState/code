import subprocess

PATH_TO_AUTOHOTKEY = r"C:\Program Files\AutoHotkey\AutoHotkey.exe"

def eval_authotkey(code):
    authotkey_process = subprocess.Popen([PATH_TO_AUTOHOTKEY, "*"],
                        shell=True,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        )
    stdout_value, stderr_value = authotkey_process.communicate(code)

    print(stderr_value)

    return stdout_value

result = eval_authotkey("""
    my_var = hello world
    msgbox % my_var
    
    ; Print to stdout: 2 methods
    ; Method 1
    FileAppend line 1`n, *

    ; Method 2
    stdout := FileOpen("*", "w")
    stdout.WriteLine("line 2")
    stdout.WriteLine("line 3")
""")

print (result)
