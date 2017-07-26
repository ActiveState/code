import win32net
import win32netcon

shinfo={}

shinfo['netname']='python test'
shinfo['type']=win32netcon.STYPE_DISKTREE
shinfo['remark']='data files'
shinfo['permissions']=0
shinfo['max_uses']=-1
shinfo['current_uses']=0
shinfo['path']='c:\\my_data'
shinfo['passwd']=''
server='servername'

win32net.NetShareAdd(server,2,shinfo)
