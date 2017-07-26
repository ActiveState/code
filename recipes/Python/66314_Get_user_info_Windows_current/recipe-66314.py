import win32api
import win32net
import win32netcon
def UserGetInfo():
    dc=win32net.NetServerEnum(None,100,win32netcon.SV_TYPE_DOMAIN_CTRL)
    user=win32api.GetUserName()
    if dc[0]:
        dcname=dc[0][0]['name']
        return win32net.NetUserGetInfo("\\\\"+dcname,user,1)
    else:
        return win32net.NetUserGetInfo(None,user,1)
if __name__=="__main__":
    print UserGetInfo()
