#!/usr/bin/env python
# -*- coding: cp1252 -*-
#figure out where the line breaks are in the file and do something with them.
import os
import sys
import getopt
import time
import string

global g_title
global l_tags
global g_index_only
g_title=""
g_encoding="utf-8"
g_encoding="cp1252"
g_encoding="iso-8859-1"
g_index_only=False
g_date_folder=""

#SVT Nyheter

def go_past_ul(s):
	s_result=s
	num_uls=0
	got_two=False
	ulpos=1
	dlpos=1
	nextpos=1
	count=len(s)
	while count>0:
		count-=1
		ulpos=s.find("ul>",ulpos+2)
		if s[ulpos-1]=="/":
			num_uls-=1
		else:
			num_uls+=1
		if num_uls>=2:got_two=True
		if ulpos<0:break
		if got_two==True and num_uls==0:
			s_result=s[ulpos+3:]
			break
	return s_result

def doc_title_name():
	s_result=""
	s_month=int(time.strftime("%m"))
	s_month=month_name(s_month)
	s_month=s_month.lower()
	s_result = "Nyheter / Actualit&eacute;s - " + time.strftime("%d") + " " + s_month + " " + time.strftime("%Y")
	return s_result

def date_folder_name():
	s_result=""
	s_month=int(time.strftime("%m"))
	s_result = os.getcwd() + os.sep + time.strftime("NY%d") + month_name(s_month) + time.strftime("%y")
	return s_result

def month_name(n_month):
	s_result=""
	if (n_month==1): s_result="JAN"
	if (n_month==2): s_result="FEV"
	if (n_month==3): s_result="MAR"
	if (n_month==4): s_result="AVR"
	if (n_month==5): s_result="MAI"
	if (n_month==6): s_result="JUN"
	if (n_month==7): s_result="JUL"
	if (n_month==8): s_result="AOU"
	if (n_month==9): s_result="SEP"
	if (n_month==10): s_result="OKT"
	if (n_month==11): s_result="NOV"
	if (n_month==12): s_result="DEC"
	return s_result

l_tags=[""]
k_style_sheet="_000_style.css"

def add_tag_to_globals(s_tag, l_tags):
	if (s_tag in l_tags)==False:
		l_tags.append(s_tag)
	return

def write_all_tags():
	fw=open("all_tags.txt", "w")
	i=0
	while i<len(l_tags):
		fw.write(l_tags[i]+"\n")
		i=i+1
	fw.close()

def left_str(s,n):
	r=""
	i=0
	b=1
	while b==1:
		if i>=n or i>=len(s) or s[i]==".":
			b=0
		if b!=0:			
			r=r+s[i]
		i=i+1
	return r		

def process_file(szFilename,iFileNum):
	global g_title

	szOutfile="~out.htm"
	f = open(szFilename, "r")

	szLine=""
	s_last_str=""
	ls=""
	s=""

	b_read_file = 1
	ft = 0;lt = 0
	r=""

	while b_read_file == 1:
		szLine=f.readline()
		szLine=szLine.replace("\n"," ")
		s=s+szLine
		ft = f.tell()
		if lt == ft:
			b_read_file=0
		lt = ft
	f.close()

	szOutfile=simplify_filename(szFilename)
	g_title=get_html_title(s)
	g_title=replace_accented_chars_with_codes(g_title)
	if len(g_title)<=4: g_title=szOutfile#"no_title"

	if s.find("<lock>")>=0 or s.find("<LOCK>")>=0 or s.find("<html class=\"lock\"")>=0:
		return szFilename

	if g_index_only==True:
		if os.path.exists(szOutfile)==False:
			os.rename(szFilename,szOutfile)
		return szOutfile

	while s<>s_last_str:
		s_last_str=s

		s=remove_ctrl_chars(s)

		s=s.replace("<!--","<!-- ")

		s=strip_comments(s)
		s=strip_copyrights(s)

		ls=""
		while s<>ls:
			ls=s
			s=s.replace("  "," ")

		ls=""
		while s<>ls:
			ls=s
			s=s.replace("<3","&hearts;")
			s=s.replace("&#9829;","&hearts;")
			s=s.replace("&hearts;","") # get rid of hearts for now.
			s=strip_tags(s)
			s=get_rid_of_useless_tags(s)

		ls=""
		while s<>ls:
			ls=s
			s=s.replace("</h1><br>","</h1>")
			s=s.replace("<br><ul>","<ul>")

		ls=""
		while s<>ls:
			ls=s
			s=s.replace("<br>&copy;","&copy;")
		s=s.replace("&copy;"," &copy;")

		ls=""
		while s<>ls:
			ls=s
			if s.endswith("<br>"):
				s=s.rstrip("<br>")

		# remove unnecessary "br" tags before and after header tags.
		ls=""
		while s<>ls:
			ls=s
			for i in range(1,7):
				s_header_tag="h"+str(i)+">"
				s=s.replace("<br><"+s_header_tag,"<"+s_header_tag)
				s=s.replace("<"+s_header_tag+"<br>","<"+s_header_tag)
				s=s.replace("</"+s_header_tag+"<br>","</"+s_header_tag)


		ls=""
		while s<>ls:
			ls=s
			for i in range(2,7):
				s_header_tag="h"+str(i)+">"
				s=s.replace("<"+s_header_tag,"<h2>")
				s=s.replace("</"+s_header_tag,"</h2>")

		ls=""
		while s<>ls:
			ls=s
			s=s.replace("<center><br>","<br><center>")
			s=s.replace("<center></center>","")
			s=s.replace("<table><br>","")
			s=s.replace("</td><br>","")
			s=s.replace("</tr><br>","")

		s=s.replace("Annons:<br>","")

		ls=""
		while s<>ls:
			ls=s
			s=s.replace("<br> ","<br>")
			s=s.replace(" <br>","<br>")
			s=s.replace("<br><br><br>","<br><br>")

		# make it start the file at the first major heading tag.
		hp=s.find("<h1>")
		if hp>0:
			s=s[hp:]+s[:hp-1] # split the file, putting the content right after the tag first.

		# for small mobile devices
		if False:
			ls=""
			while s<>ls:
				ls=s
				s=s.replace("<h2>","<b>")
				s=s.replace("</h2>","</b><br>")
				s=s.replace("<h1>","<b>")
				s=s.replace("</h1>","</b><br>")

		s=strip_script(s)
		s=replace_accented_chars_with_codes(s)

		# post processing changes

		ls=""
		while s<>ls:
			ls=s
			s=s.replace(" <tr>","<tr>")
			s=s.replace(" <td>","<td>")

	if s.find(" SVT ")>0:
		s=go_past_ul(s)

	# workaround for a SPECIFIC problem.
	s=s.replace("&lt;/iframe>","<!-- ")
	s=s.replace("\"javascript:void();\">", " -->")

	s=remove_acirc(s)
	s=s.replace("</tr>","</tr>\n")
	s=s.replace("<br>","<br>\n")
	s=s.replace("</dd><dt>", "</dd><dt>\n")

# this puts both header lines for canadian articles at the top.

	htp=0
	stp=""
	if s.endswith("</h2>"):
		htp=s.rfind("<h2>")
		if htp>=0:
			stp=s[htp:]
			s=s.replace(stp,"")

	s=stp+s
	s=s.replace("</h2><h1>","<br>")
	s=s.replace("h1>","h2>")

	s=meta_encoding_string()+s+"\n</body>\n</html>"

	os.unlink(szFilename)

	szOutfile=simplify_filename(szFilename)
	if len(szOutfile)<=8: szOutfile="no_"+szOutfile

	szOutfile=next_avail_file(szOutfile) # stops it from overwriting files in case they have the same name after simplifying with chars.
	fw=open(szOutfile, "w")
	fw.write(s)
	fw.close()
	return szOutfile

def remove_ctrl_chars(s):
	r=""
	ls=len(s)
	i=0
	c=""
	while i<ls:
		c=s[i]
		if ord(c)<32:
			c=" "
		r=r+c
		i=i+1
	return r

def remove_ext(s):
	r=s
	i=len(s)
	j=-1
	while i>=0:
		i=i-1
		if s[i]==".":
			j=i
			break
	if j>=0:
		r=s.__getslice__(0,j)
	return r

def remove_end_nums(s):
	r=s
	i=len(s)
	j=-1
	while i>=0:
		i=i-1
		if (s[i]>="a" and s[i]<="z"):
			j=i+1
			break
	if j>=0:
		r=s.__getslice__(0,j)
	return r

def get_ext(s):
	r=""
	i=len(s)
	j=-1
	while i>=0:
		i=i-1
		if s[i]==".":
			j=i
			break
	if j>=0:
		r=s.__getslice__(j+1,len(s))
	return r

def next_avail_file(s):
	r=s
	i_num=0
	while os.path.exists(s)==True:
		#s_ext=get_ext(s)
		s_ext="htm"
		r=remove_ext(s)
		r=remove_end_nums(r)
		r=r + "_" + str(i_num) + "." + s_ext
		i_num=i_num+1
		s=r
	return r

def simplify_filename(s):
	k_maxlen=40
	r=""
	i=0
	c=""
	s_ext=""
	s_file=""
	i_len=0
	s=deaccent_string(s)
	for i in range(0,len(s)):
		c=s[i]
		c=c.lower()
		if ((c>="a" and c<="z") or (c>="0" and c<="9")) or c==".":
			r=r+c
		else:
			r=r+"_"
	while r.find('__')>=0:r=r.replace("__","_")
	r=replace_accented_chars_with_codes(r)
	s_file=remove_ext(r)
	#s_ext=get_ext(r)
	#s_ext=s_ext.__getslice__(0,3)
	s_ext="htm"
	i_len=len(s_file)
	if i_len>k_maxlen:i_len=k_maxlen
	s_file=s_file.__getslice__(0,i_len)
	r=s_file + "." + s_ext
	return r

def deaccent_string(s):
	s=s.replace("Ã¤","a")
	s=s.replace("Ã¥","a")
	s=s.replace("Ã ","a")
	s=s.replace("Ã¶","o")
	s=s.replace("Ã©","e")
	s=s.replace("Ãª","e")
	s=s.replace("Ã¨","e")
	s=s.replace("Ã«","e")
	s=s.replace("Ã®","i")
	s=s.replace("Ã¹","u")
	s=s.replace("Ã»","u")
	s=s.replace("Ã„","a")
	s=s.replace("Ã…","a")
	s=s.replace("Ã–","o")
	return s

def get_rid_of_useless_tags(s):

	s=s.replace("<?xml>","")
	s=s.replace("<td><br>","<td>")
	s=s.replace("<br></td>","</td>")

	s=s.replace("<a<", "<")
	s=s.replace("<img<", "<")

	s=s.replace("</h2> </td> </tr> </table><br>", "</h2></td></tr></table>")

	s=s.replace("<small><br>","<br><small>")
	s=s.replace("<br><blockquote>","<blockquote>")
	s=s.replace("<blockquote><br>","<blockquote>")
	s=s.replace("<br></blockquote>","</blockquote>")
	s=s.replace("</blockquote><br>","</blockquote>")

	s=s.replace("&nbsp;"," ")
	s=s.replace("</title><br>","</title>")
	s=s.replace("<o>","")
	s=s.replace("</o>","")
	s=s.replace("<br> ","<br>")
	s=s.replace(" <br>","<br>")
	s=s.replace("<strong>","<b>")
	s=s.replace("</strong>","</b>")
	s=s.replace("<em>","<b>")
	s=s.replace("</em>","</b>")
	s=s.replace("<b><br></b>","<br>")
	s=s.replace("<u><br></u>","<br>")
	s=s.replace("<i><br></i>","<br>")
	s=s.replace("<b><br>","<br><b>")
	s=s.replace("<br></b>","</b><br>")
	s=s.replace("</table><br><br>","</table><br>")
	s=s.replace("<br><br><table>","<br><table>")
	s=s.replace("<!doctype>","")
	s=s.replace("</ul><br>","</ul>")
	s=s.replace("</ol><br>","</ol>")
	s=s.replace("<br></li>","</li>")
	s=s.replace("<li><br>","<li>")
	s=s.replace("<!--trackbacks>","")
	s=s.replace("<var>","")
	s=s.replace("<pe>","")
	s=s.replace("<span>","")
	s=s.replace("</span>","")
	s=s.replace("<font>","")
	s=s.replace("</font>","")
	s=s.replace("<div>","<br>")
	s=s.replace("</div>","<br>")
	s=s.replace("<p>","<br><br>")
	s=s.replace("</p><br>","<br>")
	s=s.replace("</p>","<br><br>")

	s=s.replace("<hr> ","<hr>")
	s=s.replace("<hr><hr>","<hr>")
	s=s.replace("<hr><br>","<hr>")

	s=s.replace("<hgroup>","")
	s=s.replace("</hgroup>","")

	s=s.replace("<meta>","")
	s=s.replace("<area>","")
	s=s.replace("<map>","")
	s=s.replace("</map>","")
	s=s.replace("<img>","")
	s=s.replace("<a>","")
	s=s.replace("</a>","")
	s=s.replace("<!-->","")
	s=s.replace("<link>","")
	s=s.replace("<aside>","")
	s=s.replace("</aside>","")
	s=s.replace("<form>","")
	s=s.replace("</form>","")
	s=s.replace("<input>","")
	s=s.replace("<![endif]>","")
	s=s.replace("<script>","<textarea>")
	s=s.replace("</script>","</textarea>")
	s=s.replace("<style>","<textarea>")
	s=s.replace("</style>","</textarea>")
	s=s.replace("<iframe>","")
	s=s.replace("</iframe>","")
	s=s.replace("<param>","")
	s=s.replace("</param>","")
	s=s.replace("<embed>","")
	s=s.replace("</embed>","")
	s=s.replace("<object>","")
	s=s.replace("</object>","")
	s=s.replace("<noscript>","")
	s=s.replace("</noscript>","")
	s=s.replace("<html>","")
	s=s.replace("</html>","")
	s=s.replace("<body>","")
	s=s.replace("</body>","")
	s=s.replace("<head>","")
	s=s.replace("</head>","")
	s=s.replace("<nav>","")
	s=s.replace("</nav>","")
	s=s.replace("<header>","")
	s=s.replace("</header>","")
	s=s.replace("<article>","")
	s=s.replace("</article>","")
	s=s.replace("<section>","")
	s=s.replace("</section>","")
	s=s.replace("<figure>","")
	s=s.replace("</figure>","")
	s=s.replace("<figcaption>","")
	s=s.replace("</figcaption>","")
	s=s.replace("<footer>","")
	s=s.replace("</footer>","")
	s=s.replace("<panel>","")
	s=s.replace("</panel>","")
	s=s.replace("<center>","")
	s=s.replace("</center>","")
	s=s.replace("&amp;quot;","\"")
	s=s.replace("\xEF\xBB\xBF","") #gets rid of weird symbols at the beginning of files.
	return s

def replace_accented_chars_with_codes(s):

# russian
	s=s.replace("\xD0\x27","B")# D0 =-D
	s=s.replace("\xD0\xB5","e")# 
	s=s.replace("\xD1\x80","p")# D1 =N~
	s=s.replace("\xD0\xBD","H")

# normal
	s=s.replace("\xE2\x89\xA5","&#8805;")
	s=s.replace("\xE2\x89\xA4","&#8804;")
	s=s.replace("\xC5\x91","&#337;")
	s=s.replace("\xC5\xB1","&#369;")
	s=s.replace("\xE2\xAC\xA8","&mdash;")
	s=s.replace("\xEF\xBF\xBD","&nbsp;")
	s=s.replace("\xE2\x99\xA5","&hearts;")
	s=s.replace("\xE2\x82\xAC","&euro;")

	s=s.replace("\xE2\x80\x89"," ")
	s=s.replace("\xE2\x80\xBA","&gt;")
	s=s.replace("\xE2\x80\xA6","...")
	s=s.replace("\xE2\x80\xA2","&bull;")
	s=s.replace("\xE2\x80\x93","&ndash;")
	s=s.replace("\xE2\x80\x94","&mdash;")
	s=s.replace("\xE2\x80\x98","'")
	s=s.replace("\xE2\x80\x99","'")
	s=s.replace("\xE2\x80\x9C","\"")
	s=s.replace("\xE2\x80\x9D","\"")

	s=s.replace("\xE2\x80","&mdash;") # need Z with caron

	s=s.replace("\xE2\x98","&#9788;")
	s=s.replace("\xC2\xB0","&deg;")
	s=s.replace("\xC2\xA0"," ")
	s=s.replace("\xC2\xAD","&shy;")
	s=s.replace("\xC2\xA4","&bull;")
	s=s.replace("\xE2\x96\xA0","&bull;")
	s=s.replace("\xC2\xAE","&reg;")
	s=s.replace("\xC2\xBB","&raquo;")
	s=s.replace("\xC2\xAB","&laquo;")
	s=s.replace("\xC2\xB2","&sup2;")
	s=s.replace("\xC2\xB3","&sup3;")
	s=s.replace("\xC2\xB9","&sup1;")
	s=s.replace("\xC2\xB4","'")
	s=s.replace("\xC2\xBD","&frac12;")
	s=s.replace("\xC3\xBC","&uuml;")
	s=s.replace("\xC3\xBA","&uacute;")
	s=s.replace("\xC3\xA0","&agrave;")
	s=s.replace("\xC3\xA1","&aacute;")
	s=s.replace("\xC3\xA2","&acirc;")
	s=s.replace("\xC3\xA3","&atilde;")
	s=s.replace("\xC3\xA4","&auml;")
	s=s.replace("\xC3\xA5","&aring;")
	s=s.replace("\xC3\xA6","&aelig;")
	s=s.replace("\xC3\xA7","&ccedil;")
	s=s.replace("\xC3\xAC","&igrave;")
	s=s.replace("\xC3\xAD","&iacute;")
	s=s.replace("\xC3\xAE","&icirc;") 
	s=s.replace("\xC3\xAF","&iuml;")
	s=s.replace("\xC3\xB0","&eth;")
	s=s.replace("\xC3\xB1","&ntilde;")
	s=s.replace("\xC3\xB2","&ograve;")
	s=s.replace("\xC3\xB3","&oacute;")
	s=s.replace("\xC3\xB5","&otilde;")
	s=s.replace("\xC3\xB4","&ocirc;")
	s=s.replace("\xC3\xB8","&oslash;")
	s=s.replace("\xC3\xB6","&ouml;")
	s=s.replace("\xC3\xB9","&ugrave;")
	s=s.replace("\xC3\xBE","&thorn;")
	s=s.replace("\xC3\xA9","&eacute;")
	s=s.replace("\xC3\xA8","&egrave;")
	s=s.replace("\xC3\xAA","&ecirc;")
	s=s.replace("\xC3\xAB","&euml;")
	s=s.replace("\xC3\xBB","&ucirc;")
	s=s.replace("\xC3\xB1","&ntilde;")
	s=s.replace("\x00\x9C","&oelig;")
	s=s.replace("\xC2\x9C","&oelig;")
	s=s.replace("\xC5\x22","&oelig;")
	s=s.replace("\xC5\x27","&OElig;")
	s=s.replace("\xC5\x93","&oelig;")
	s=s.replace("\xC2\xA9","&copy;")
	s=s.replace("\xC2\xA3","&pound;")
	s=s.replace("\xC3\x87","&Ccedil;")
	s=s.replace("\xC3\x84","&Auml;")
	s=s.replace("\xC3\x85","&Aring;")
	s=s.replace("\xC3\x82","&Acirc;")
	s=s.replace("\xC3\x80","&Agrave;")
	s=s.replace("\xC3\x81","&Aacute;")
	s=s.replace("\xC3\x88","&Egrave;")
	s=s.replace("\xC3\x89","&Eacute;")
	s=s.replace("\xC3\x8A","&Ecirc;")
	s=s.replace("\xC3\x8B","&Euml;")
	s=s.replace("\xC3\x8C","&Igrave;")
	s=s.replace("\xC3\x8D","&Iacute;")
	s=s.replace("\xC3\x8E","&Icirc;")
	s=s.replace("\xC3\x8F","&Iuml;")
	s=s.replace("\xC3\x94","&Ocirc;")
	s=s.replace("\xC3\x96","&Ouml;")
	s=s.replace("\xC3\x99","&Ugrave;") #?
	s=s.replace("\xC3\x9C","&Uuml;") #?

	#s=s.replace("\xBF","")
	s=s.replace("\xC0","&Agrave;")
	s=s.replace("\xC7","&Ccedil;")
	s=s.replace("\xC8","&Egrave;")
	s=s.replace("\xC9","&Eacute;")
	s=s.replace("\xD4","&Ocirc;")
	s=s.replace("\xD9","&Ugrave;")
	s=s.replace("\xDB","&Ucirc;")
	s=s.replace("\xE0","&agrave;")
	s=s.replace("\xE2","&acirc;")
	s=s.replace("\xE7","&ccedil;")
	s=s.replace("\xE8","&egrave;")
	s=s.replace("\xE9","&eacute;")
	s=s.replace("\xEA","&ecirc;")
	s=s.replace("\xEB","&euml;")
	s=s.replace("\xEE","&icirc;")
	s=s.replace("\xEF","&iuml;")
	s=s.replace("\xF4","&ocirc;")
	s=s.replace("\xF9","&ugrave;")
	s=s.replace("\xFB","&ucirc;")
	s=s.replace("\n"," ")
	s=s.replace("\r"," ")
	s=s.replace("\t"," ")
	s=s.replace(" Â "," ")
	s=s.replace("\x80","&euro;")
	s=s.replace("\x85","...")
	s=s.replace("\x2D","-")
	s=s.replace("\u002D","-")
	s=s.replace("\x92","'")
	s=s.replace("\x93","\"")
	s=s.replace("\x94","\"")
	s=s.replace("\xBB","&raquo;")
	s=s.replace("\xAB","&laquo;")

	s=s.replace("\xA0"," ")
	s=s.replace("&rsquo;","\'")
	s=s.replace("&lsquo;","\'")
	s=s.replace("&rdquo;","\"")
	s=s.replace("&ldquo;","\"")

	s=s.replace(" \xC3 "," &agrave; ")
	s=s.replace("'\xC3 ","'&agrave; ")

	return s

def strip_script(s):
	r=""
	cp=0
	lbp=1
	rbp=0
	while lbp>=0:
		lbp=s.find("<textarea",cp)
		if lbp>=0:
			while cp<lbp: # copy up to and including.
				r=r+s[cp]
				cp=cp+1
			rbp=s.find("</textarea>",lbp+10) # was lbp+1
			if rbp>lbp:
				cp=rbp+11
			else:
				cp=cp+10
	while cp<len(s):
		r=r+s[cp]
		cp=cp+1
	return r


def meta_encoding_string():
	r="<!DOCTYPE html>\n<html class=\"lock\">\n"
	r+="<head>\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=" + g_encoding + "\" />"
	r+="\n"
	r+="<link rel=\"stylesheet\" type=\"text/css\" href=\""+k_style_sheet+"\">\n"
	r+="</head>\n"
	r+="<body>\n"
	return r

def char_code_table():
	f = open("charmap.htm", "w")
	i=32
	s=""
	f.write(meta_encoding_string())
	f.write("<table border=1 cellspacing=0 cellpadding='4'>")
	while i<=255:
		s="<tr><td>" + hex(i).upper() + "</td><td>" + "&#" + str(i) + ";</td></tr>"
		f.write(s)
		i=i+1
	f.write("</table></body></html>")
	return

def get_html_title(s):
	tp=0
	te=0
	r=""
	tp=s.find("<title>")
	te=s.find("</title>",tp)
	if tp>0 and te>0 and te>tp:
		if te-tp<200:
			r=s[tp+7:te]
	return r

def strip_tags(s):
	r=""
	c=""
	s_tag=""
	s_last_tag=""
	tag_char_count=0
	cp=0
	b_intag=False
	b_afterspace=False
	while cp<len(s):
		c=s[cp];
		if c=="<":
			tag_char_count=0
			b_intag=True
			b_afterspace=False
		if b_intag==True:
			c=c.lower()
			tag_char_count=tag_char_count+1
			if (c==" " or c==":") and b_afterspace==False:b_afterspace=True
			if tag_char_count>2 and c=="/":c=""
			if b_afterspace==True and c!=">":c=""
			s_tag=s_tag+c

		if c==">" and b_intag==True:
			b_intag=False
			if s_tag==inverse_tag(s_last_tag):
				gt_index=r.rfind("<")
				if gt_index>=0:
					r=r[0:gt_index]
			else:
				add_tag_to_globals(s_tag, l_tags)
				r=r+s_tag
			s_last_tag=s_tag
			s_tag=""
			c=""
		if b_intag==True and b_afterspace==True:c=""
		if b_intag==False:
			if c!=" " and c!="":s_last_tag=""
			r=r+c
		cp=cp+1
	return r

def inverse_tag(s):
	s_result=""
	if len(s)>1:
		if s[1]=="/":
			s_result=s_result.replace("/","")
		else:
			s_result="</"+s[1:]
		return s_result

def strip_comments(s):
 # this still gets stuck !
 r=""
 ls=""
 ap=0
 rp=0
 ap=s.find("<!--")
 while ap>=0:
	ap=s.find("<!--")
	rp=s.find("-->",ap+3)
	if ap>0 and rp>ap:
	 s=s[:ap]+s[rp+3:]
	else:
	 break
 return s

def strip_copyrights(s):
 r=""
 ap=0
 rp=0
 ap=s.find("&copy;")
 while ap>=0:
	ap=s.find("&copy;")
	rp=s.find("<",ap)
	if ap>0 and rp>ap:
	 s=s[:ap]+s[rp:]
	else:
	 break
 return s

# gets rid of annoying "Ã‚"s.
def remove_acirc(s):
	r=""
	ls=len(s)
	i=0
	c=""
	lc=""
	b=False
	bp=False
	while i<ls:
		c=s[i]
		bp=True
		if lc=="\xC2":
			if c=="\x22":bp=False
			if c=="\x96":bp=False
			if not is_letter(c):bp=False
		if bp:r=r+lc
		i=i+1
		lc=c
	r=r+lc
	return r

def is_html_file(s):
	b=False
	if (s.endswith(".htm")==True or s.endswith(".html")==True or s.endswith(".dhtml")==True or s.endswith(".dht")==True): b=True
	if s.endswith(".ab")==True: b=True
	if s.endswith(".shtml")==True: b=True
	if s.endswith(".aspx")==True: b=True
	return b

def is_letter(s):
	b=False
	if (s>="a" and s<="z"): b=True
	if (s>="A" and s<="Z"): b=True
	return b

# loop through all of the files in the directory
def main():

	g_date_folder=date_folder_name()

	num_html_files=0
	k_index_file="_000_index.htm"
	ls=os.listdir(".")
	ls.sort()

	r=""
	s_new_filename=""
	s_link_name=""

	i=0
	while i<len(ls):
		szFilename=ls[i]
		uFilename=str(szFilename)
		uFilename=uFilename.lower()
		if is_html_file(uFilename) and uFilename<>k_index_file:
			num_html_files=num_html_files+1
		i=i+1

	s_progress="0"
	i=0
	nth_html_file=0
	while i<len(ls):
		szFilename=ls[i]
		uFilename=str(szFilename)
		uFilename=uFilename.lower()
		if is_html_file(uFilename) and uFilename<>k_index_file:
			nth_html_file=nth_html_file+1
			print s_progress + " " + szFilename[:30]
			s_new_filename=""
			if os.path.exists(szFilename)==True:
				s_new_filename=process_file(szFilename,i)
			if s_new_filename!="":
				s_link_name=s_new_filename
				if g_title!="":s_link_name=g_title
				s_link="<a href=\"" + s_new_filename + "\">" + s_link_name + "</a>"
				if s_link.find("<i>")>=0:s_link=s_link+"</i>"
				if s_link.find("<b>")>=0:s_link=s_link+"</b>"
				s_link=s_link+"<br>\n"
				r=r+s_link
				#show the progress indicator.
				if num_html_files>0:
					s_progress="%.2f" % (float(nth_html_file)/float(num_html_files)*float(100))
				else:
					s_progress="0"
				curr_time=os.times()[0]
				last_time=os.times()[0]
				while curr_time==last_time:
					last_time=os.times()[0]
					# progress was here.
		i=i+1

	if nth_html_file>0:
		if not os.path.exists(g_date_folder):
			os.mkdir(g_date_folder)

		r=meta_encoding_string()+"<style>a{text-decoration:none}</style>"+"<title>"+doc_title_name()+"</title>"+"<center><table><tr><td>"+r
		fw=open(k_index_file, "w")
		fw.write(r)
		fw.write("</td></tr></table>")
		fw.close()

		fw=open(g_date_folder + os.sep + k_style_sheet, "w")

		#fw.write(".specialbar{background-color:maroon;color:white;font-weight:bold;text-align:center;}\n")
		fw.write("html{font-size:14pt;width:75%;margin:auto;padding:6pt;border:solid black 1px;font-family:Sans}\n")
		fw.write("td{vertical-align:top;}\n")
		fw.write("h1{color:navy;font-size:18pt;}\n")
		fw.write("h2{color:navy;font-size:18pt;}\n")
		fw.write("a{color:navy;font-size:14pt;}\n")
		fw.close()
	else:
		print "Nothing to do"

	if True:
		i=0
		ls=os.listdir(".")
		ls.sort()
		while i<len(ls):
			szFilename=ls[i]
			if is_html_file(szFilename):
				s_moved_filename = g_date_folder + os.sep + szFilename
				if os.path.exists(s_moved_filename)==False:
					os.rename(szFilename, s_moved_filename)
			i=i+1

	#write_all_tags()

	print "done"
	return

#print "Warning : back up all files before proceeding"
main()
