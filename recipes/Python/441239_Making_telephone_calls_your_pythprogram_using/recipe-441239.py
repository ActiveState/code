import urllib
import time


class Voicent:
	def __init__(self, host="localhost", port="8155"):
		self.host_ = host
		self.port_ = port

	def callText(self, phoneno, text, selfdelete):
		urlstr = "/ocall/callreqHandler.jsp"

		param = {'info' : 'simple text call',
                         'phoneno' : phoneno,
			 'firstocc' : 10,
			 'txt' : text,
			 'selfdelete' : selfdelete}

		rcstr = self.postToGateway(urlstr, param)
		return self.getReqId(rcstr)

	def callAudio(self, phoneno, filename, selfdelete):
		urlstr = "/ocall/callreqHandler.jsp"

		param = {'info' : 'simple audio call',
			 'phoneno' : phoneno,
			 'firstocc' : 10,
			 'audiofile' : filename,
        		 'selfdelete' : selfdelete}

		rcstr = self.postToGateway(urlstr, param)
		return self.getReqId(rcstr)

	def callStatus(self, reqId):
		urlstr = "/ocall/callstatusHandler.jsp"
		param = {'reqid' : reqId}
		rcstr = self.postToGateway(urlstr, param)
		
		if (rcstr.find("^made^") != -1):
			return "Call Made"

		if (rcstr.find("^failed^") != -1):
			return "Call Failed"

		if (rcstr.find("^retry^") != -1):
			return "Call Will Retry"

		return ""

	def callRemove(self, reqId):
		urlstr = "/ocall/callremoveHandler.jsp"
		param = {'reqid' : reqId}
		rcstr = self.postToGateway(urlstr, param)

	def callTillConfirm(self, vcastexe, vocfile, wavfile, ccode):
		urlstr = "/ocall/callreqHandler.jsp"

		cmdline = "\""
		cmdline += vocfile
		cmdline += "\""
		cmdline += " -startnow"
		cmdline += " -confirmcode "
		cmdline += ccode
		cmdline += " -wavfile "
		cmdline += "\""
		cmdline += wavfile
		cmdline += "\""

		param = {'info' : 'Simple Call till Confirm',
			 'phoneno' : '1111111',
			 'firstocc' : 10,
			 'selfdelete' : 0,
			 'startexec' : vcastexe,
			 'cmdline' : cmdline}

		self.postToGateway(urlstr, param)


	def postToGateway(self, urlstr, poststr):
		params = urllib.urlencode(poststr)
		url = "http://" + self.host_ + ":" + self.port_ + urlstr
		f = urllib.urlopen(url, params)
		return f.read()

	def getReqId(self, rcstr):
		index1 = rcstr.find("[ReqId=")
		if (index1 == -1):
			return ""
		index1 += 7

		index2 = rcstr.find("]", index1)
		if (index2 == -1):
			return ""

		return rcstr[index1:index2]



#
# Uncomment out the following for your test
#
#put your own number there
#phoneno = "111-2222"
#
#v = Voicent()
#v.callText(phoneno, "hello, how are you", "1")

#reqid = v.callAudio(phoneno, "C:/Program Files/Voicent/MyRecordings/sample_message.wav", "0")

#while (1):
#	time.sleep(1)
#	status = v.callStatus(reqid)
#	if (status != ""):
#		break

#v.callRemove(reqid)

#v.callTillConfirm("C:/Program Files/Voicent/BroadcastByPhone/bin/vcast.exe",
#                  "C:/temp/testctf.voc",
#                  "C:/Program Files/Voicent/MyRecordings/sample_message.wav",
#                  "1234")
