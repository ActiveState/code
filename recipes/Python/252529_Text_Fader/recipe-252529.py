##################################################################################
##
##	Author:		Premshree Pillai
##	Date:		12/12/03	
##	File Name:	text-fader.py
##	Description:    -Text Fader
##                      -Use this script to create a text fading effect
##                       See the file http://qiksearch.com/python/text-fader.htm 
##			 for an example generated using this script
##	Website:	http://www.qiksearch.com
##	Category:	Utilities
##
##################################################################################

import math

TF_hexChars = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]

def TF_dec2hex(decVal):
	return(TF_hexChars[decVal >> 4] + TF_hexChars[decVal & 15])

def TF_hex2dec(hexVal):
	return(int(hexVal,16))

def TextFade(TF_text,TF_font,TF_fontSize,TF_isBold,TF_isItalic,intColor,finalColor):
	TF_text_arr = TF_text
	rVal=TF_hex2dec(intColor[0:2])
	gVal=TF_hex2dec(intColor[2:4])
	bVal=TF_hex2dec(intColor[4:6])
	r_step=int(math.floor((TF_hex2dec(finalColor[0:2])-rVal)/(len(TF_text_arr))))
	g_step=int(math.floor((TF_hex2dec(finalColor[2:4])-gVal)/(len(TF_text_arr))))
	b_step=int(math.floor((TF_hex2dec(finalColor[4:6])-bVal)/(len(TF_text_arr))))

	if(TF_isBold):
		TF_isBold_content = "<b>"
		TF_isBold_end_content = "</b>"
	else:
		TF_isBold_content = ""
		TF_isBold_end_content = ""

	if(TF_isItalic):
		TF_isItalic_content = "<i>"
		TF_isItalic_end_content = "</i>"
	else:
		TF_isItalic_content = ""
		TF_isItalic_end_content = ""

	count = 0
	outStr = ""
	for i in TF_text_arr:
		count = count + 1
		outStr = outStr + '<font color="#' + TF_getColor(rVal,gVal,bVal,r_step,g_step,b_step) + '" face="' + TF_font + '" size="' + TF_fontSize + '">' + TF_isBold_content + TF_isItalic_content + i + TF_isItalic_end_content + TF_isBold_end_content + '</font>'
		if(count < len(TF_text_arr)):
			if(TF_text_arr[count] != " "):
				rVal = rVal + r_step
				gVal = gVal + g_step
				bVal = bVal + b_step
	return outStr

def TF_getColor(rcol,gcol,bcol,rstep,gstep,bstep):
	rcol = rcol + rstep
	gcol = gcol + gstep
	bcol = bcol + bstep
	return(TF_dec2hex(rcol)+TF_dec2hex(gcol)+TF_dec2hex(bcol));

def getText():
	global text, bold, italics, face, size
	text = raw_input("Enter the text you want to fade: ")
	if(len(text) == 0):
		getText()
	else:
		face = raw_input("Font  face (Verdana, Arial, Trebuchet MS..., or <enter> for default)? ")
		size = raw_input("Font  size (1, 2, 3, 4..., or <enter> for default)? ")
		bold = raw_input("Bold text (1=yes, 0=no)? ")
		italics = raw_input("Italicize text (1=yes, 0=no)? ")
		if(len(face) == 0):
			face = "verdana,arial,helvetica"
		if(len(size) == 0):
			size = "3"
		try:
			bold = int(bold)
		except ValueError:
			bold = 0
		try:
			italics = int(italics)
		except ValueError:
			italics = 0

def getStart():
	global startColor
	startColor = raw_input("Enter start color (e.g., CCCCFF): ")
	if(len(startColor) != 6):
		print "ERROR! Color must be of the form RRGGBB (e.g., CCCCFF)"
		getStart()
	try:
		temp = int(startColor,16)
	except ValueError:
		print "ERROR! Color must be a valid Hex of the form RRGGBB (e.g., CCCCFF)"
		getStart()

def getEnd():
	global endColor
	endColor = raw_input("Enter end color (e.g., 000066): ")
	if(len(endColor) != 6):
		print "ERROR! Color must be of the form RRGGBB (e.g., 000066)"
		getEnd()
	try:
		temp = int(endColor,16)
	except ValueError:
		print "ERROR! Color must be a valid Hex of the form RRGGBB (e.g., 000066)"
		getEnd()

def ask():
	global fileName, fp
	fileName = raw_input("Enter name of HTML file to be created (e.g., fade.htm): ")
	try:
		fp = open(fileName,"r")
		flag = raw_input("File exists. Rewrite (1=yes, 0=no)? ")
		if(flag == "1"):
			fp.close()
			fp = open(fileName,"w")
			fp.write(TextFade(text,face,size,bold,italics,startColor,endColor))
			fp.close()
		else:
			ask()
	except IOError:
		fp = open(fileName,"w")
		fp.write(TextFade(text,face,size,bold,italics,startColor,endColor))
		fp.close()

print "\n\tPython Text Fader by Premshree Pillai"
print "\t     [http://www.qiksearch.com/]"
print "\t#####################################\n"

getText()
getStart()
getEnd()
ask()

print "\n", fileName, "created!"
print "Press <enter> to exit..."
if(raw_input()):
	exit
