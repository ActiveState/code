# HtmlMail python class
# Compose HTML mails from URLs or local files with all images included
#
# Author: Catalin Constantin <dazoot@gmail.com>

import sys, os, urllib2, urlparse
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from email.MIMEMultipart import MIMEMultipart
import email, re

class HtmlMail:
	def __init__(self, location, encoding="iso-8859-1"):
		self.location=location
		if location.find("http://")==0:
			self.is_http=True
		else:
			self.is_http=False
		
		self.encoding=encoding

		self.p1=re.compile("(<img.*?src=\")(.*?)(\".*?>)", re.IGNORECASE|re.DOTALL)
		self.p2=re.compile("(<.*?background=\")(.*?)(\".*?>)", re.IGNORECASE|re.DOTALL)
		self.p3=re.compile("(<input.*?src=\")(.*?)(\".*?>)", re.IGNORECASE|re.DOTALL)
		
		self.img_c=0

	def set_log(self,log):
		self.log=log
	
	def _handle_image(self, matchobj):
		img=matchobj.group(2)
		if not self.images.has_key(img):
			self.img_c+=1
			self.images[img]="dazoot-img%d" % self.img_c
		return "%scid:%s%s" % (matchobj.group(1), self.images[img], matchobj.group(3))
		
	def _parse_images(self):
		self.images={}
		self.content=self.p1.sub(self._handle_image, self.content)
		self.content=self.p2.sub(self._handle_image, self.content)
		self.content=self.p3.sub(self._handle_image, self.content)
		return self.images
		
	def _read_image(self, imglocation):
		if self.is_http:
			img_url=urlparse.urljoin(self.location, imglocation)
			content=urllib2.urlopen(img_url).read()
			return content
		else:
			return file(imglocation, "rb").read()

	def get_msg(self):
		if self.is_http:
			content=urllib2.urlopen(self.location).read()
		else:
			content=file(self.location, "r").read()
		self.content=content
		
		msg=MIMEMultipart("related")
		images=self._parse_images()

		tmsg=MIMEText(self.content, "html", self.encoding)
		msg.attach(tmsg)

		for img in images.keys():
			img_content=self._read_image(img)
			img_msg=MIMEImage(img_content)
			img_type, img_ext=img_msg["Content-Type"].split("/")

			del img_msg["MIME-Version"]
			del img_msg["Content-Type"]
			del img_msg["Content-Transfer-Encoding"]

			img_msg.add_header("Content-Type", "%s/%s; name=\"%s.%s\"" % (img_type, img_ext, images[img], img_ext))
			img_msg.add_header("Content-Transfer-Encoding", "base64")
			img_msg.add_header("Content-ID", "<%s>" % images[img])
			img_msg.add_header("Content-Disposition", "inline; filename=\"%s.%s\"" % (images[img], img_ext))
			msg.attach(img_msg)

		return msg

if __name__=="__main__":
	# test the class here
	import smtplib
	hm=HtmlMail("http://www.egirl.ro/newsletter/december2005_2/")
	msg=hm.get_msg()
	msg["Subject"]="Egirl Newsletter"
	msg["From"]="Catalin Constantin <dazoot@gmail.com>"
	msg["To"]="dazoot@gmail.com"
	
	s=smtplib.SMTP("localhost")
	s.sendmail("dazoot@gmail.com", msg["To"], msg.as_string())
	s.quit()
	
