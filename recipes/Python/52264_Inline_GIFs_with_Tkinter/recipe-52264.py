# this code fragment will convert a GIF to python source code
import base64
print "icon='''\\\n" + base64.encodestring(open("icon.gif", "rb").read()) + "'''"

# here's the result
icon='''R0lGODdhFQAVAPMAAAQ2PESapISCBASCBMTCxPxmNCQiJJya/ISChGRmzPz+/PxmzDQyZDQyZDQy
ZDQyZCwAAAAAFQAVAAAElJDISau9Vh2WMD0gqHHelJwnsXVloqDd2hrMm8pYYiSHYfMMRm53ULlQ
HGFFx1MZCciUiVOsPmEkKNVp3UBhJ4Ohy1UxerSgJGZMMBbcBACQlVhRiHvaUsXHgywTdycLdxyB
gm1vcTyIZW4MeU6NgQEBXEGRcQcIlwQIAwEHoioCAgWmCZ0Iq5+hA6wIpqislgGhthEAOw==
'''

# to use this in Tkinter:
import Tkinter
root = Tkinter.Tk()
iconImage=Tkinter.PhotoImage(master=root, data=icon)
Tkinter.Button(image=iconImage).pack()
