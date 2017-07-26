#!/usr/bin/python

import sys,os

hist=[]

def actually_write():
	global hist
	sys.stdout.write("\x1b[%sm"%(";".join(hist)))

def o(msg):
	global hist
	msg="%02i"%msg
	hist.append(msg)
	actually_write()

def undo():
	global hist
	hist.pop()
	actually_write()

def reset():
	global hist
	hist=[]
	sys.stdout.write("\x1bc\x1b[!p\x1b[?3;4l\x1b[4l\x1b>")
	default()

def default():
	o(10) # in case someone called o(12) by mistake :P
	o(0)

def clear():
	sys.stdout.write("\x1b[H\x1b[2J")

def move(y,x):
	sys.stdout.write("\x1b[%i;%iH"%(y+1,x+1))

def up():
	sys.stdout.write("\x1b[A")

def down():
	sys.stdout.write("\x1b[B")

def right():
	sys.stdout.write("\x1b[C")

def left():
	sys.stdout.write("\x1b[D")

def endline():
	sys.stdout.write("\x1b[K")

def cursorinvisible():
	sys.stdout.write("\x1b[?25l")

def cursornormal():
	sys.stdout.write("\x1b[?12l\x1b[?25h")

def cursorveryvisible():
	sys.stdout.write("\x1b[?12;25h")

def deletelines(lines=1):
	sys.stdout.write("'\x1b[%iM"%lines)

def scrolldown():
	sys.stdout.write("\x1bM")

def cols():
	return int(os.popen("tput cols").read().strip())

def lines():
	return int(os.popen("tput lines").read().strip())

def savecursor():
	sys.stdout.write("\x1b7")

def restorecursor():
	sys.stdout.write("\x1b8")

def bold():
	o(1)

def hidden():
	o(2)

def underline():
	o(4)

def blink():
	o(5)

def reverse():
	o(7)

def formatting():
	o(12)

def black():
	o(30)

def red():
	o(31)

def green():
	o(32)

def orange():
	o(33)

def blue():
	o(34)

def magenta():
	o(35)

def cyan():
	o(36)

def white():
	o(37)

def bgred():
	o(41)

def bggreen():
	o(42)

def bgorange():
	o(43)

def bgblue():
	o(44)

def bgmagenta():
	o(45)

def bgcyan():
	o(46)

def bgwhite():
	o(47)

def put(line,indent,msg):
	move(line,indent)
	sys.stdout.write(msg)

def center(line,msg):
	columns=cols()
	indent=(columns-len(msg))/2
	put(line,indent,msg)
	return line,indent+len(msg)

def wrap(*args):
	"wrap(line, [[lmargin,] rmargin,] msg)"
	if len(args)==4:
		line,lmargin,rmargin,msg=args
	elif len(args)==3:
		line,rmargin,msg=args
		lmargin=0
	elif len(args)==2:
		line,msg=args
		lmargin,rmargin=0,0
	elif len(args)<2:
		raise TypeError,"wrap() takes at least two arguments"
	else:
		raise TypeError,"wrap() takes at most four arguments"
	line_length=cols()-lmargin-rmargin
	msg=list(msg)
	curr_indent=0
	curr_line=line
	char=msg.pop(0)
	while 1:
		if line_length-curr_indent<1:
			put(curr_line,lmargin+curr_indent,'\n')
			curr_line+=1
			curr_indent=0
			put(curr_line,lmargin,char)
		else:
			put(curr_line,lmargin+curr_indent,char)
			curr_indent+=1
			if len(msg)==0:
				break
			char=msg.pop(0)
	return curr_line,lmargin+curr_indent

def wordwrap(*args):
	"wordwrap(line, [[lmargin,] rmargin,] msg)"
	if len(args)==4:
		line,lmargin,rmargin,msg=args
	elif len(args)==3:
		line,rmargin,msg=args
		lmargin=0
	elif len(args)==2:
		line,msg=args
		lmargin,rmargin=0,0
	elif len(args)<2:
		raise TypeError,"wordwrap() takes at least two arguments"
	else:
		raise TypeError,"wordwrap() takes at most four arguments"
	line_length=cols()-lmargin-rmargin
	msg=msg.split()
	curr_indent=0
	curr_line=line
	word=msg.pop(0)
	while 1:
		if line_length<len(word): # word is longer than allowed line
			put(curr_line,lmargin,word[:line_length]) # wrap by letter
			word=word[line_length:]
			put(curr_line,lmargin+curr_indent,'\n')
			curr_line+=1
			curr_indent=0
		elif line_length-curr_indent<len(word): # word cannot fit on remainder
			put(curr_line,lmargin+curr_indent,'\n') # of line -- wrap by word
			curr_line+=1
			curr_indent=0
			put(curr_line,lmargin,word)
		else: # word fits on line
			put(curr_line,lmargin+curr_indent,word)
			curr_indent+=len(word)+1
			if len(msg)==0:
				break
			word=msg.pop(0)
	return curr_line,lmargin+curr_indent

def main():
	reset()
	bgblue()
	white()
	bold()
	clear()
	reverse()
	center(5,' Windows ')
	undo()
	line,col=wordwrap(7,7,8,"Windows crashed again. I am the Blue Screen of Death. No one hears your screams.")
	print
	put(line+2,11,"*")
	line,col=wordwrap(line+2,14,8,"Press any key to terminate the application.")
	put(line+1,11,"*")
	line,col=wordwrap(line+1,14,8,"Press CTRL+ALT+DEL again to restart your computer. You will lose any unsaved data in all applications.")
	line,col=center(line+3,"Press any key to continue")
	move(line,col+1)
	endline()
	raw_input()
	reset()

if __name__=="__main__":
	main()
