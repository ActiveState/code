import string

class multi_replace:
    def __init__(self,keep=[],debug=''):
        self.keep={};self.debug=0
        if debug: self.debug=1
        if keep:
            for i in keep: self.keep[i]=1
        else:
            #keep all keyboard characters plus whitespace
            for i in string.printable: self.keep[i]=1
        
            #remove space characters except for ' '
            for i in string.whitespace:
                if i==' ': continue #whitespace is valid
                if i in self.keep: del self.keep[i]

    def replace(self,line,new_char):
        bad=0;changed=0
        #keep on replacing until there are no bad characters left
        while 1:
            clean=1
            for c in line:
                if c not in self.keep:
                    clean=0
                    line=line.replace(c,new_char)
                    changed=1
                    #cannot continue replacing since line has changed w/for loop
                    break
            #break the while loop if nothing bad was found
            if clean: break
            if self.debug and changed: print line
        return line
