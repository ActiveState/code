import pythoncom
import win32com.client

class NTUser:
# Uses ADSI to change password under user privileges	
	def __init__(self, userid):
		self.adsiNS = win32com.client.Dispatch('ADsNameSpaces')
		Userpath = "WinNT://DOMAIN/" + userid + ",user"
		self.adsNTUser = self.adsiNS.GetObject("", Userpath)

	def reset(self, OldPasswd, NewPasswd):
		self.adsNTUser.ChangePassword(OldPasswd, NewPasswd)

# You could use the following instead if you're running under admin privileges
#		self.adsNTUser.SetPassword(NewPasswd)

		print "NT Password change was successful."

try:
	nt = NTUser(account)
	nt.reset(OldPassword, NewPassword)

except pythoncom.com_error, (hr, msg, exc, arg):
	scode = hex(exc[5])
	print "NT Password change has failed."

	if (scode == "0x8007005"):
		print "Your NT Account is locked out."
	elif (scode == "0x80070056"):
		print "Invalid Old NT Password."
	elif (scode == "0x800708ad"):
		print "The specified NT Account does not exist."
	elif (scode == "0x800708c5"):
		print "Your new password cannot be the same as any of your previous passwords."
		print "Your new password must also meet the domain's password uniqueness policy."
	else:
		print "ADSI Error - %s: %s, %s\n" % (hex(hr), msg, scode)
