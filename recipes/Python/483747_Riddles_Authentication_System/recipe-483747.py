##################################################################################################################
##################################################################################################################
##
## RAS- Riddle's Authentication System (04/08/2006)
## This Python file contains the skeleton functions for RAS.
## If you want to use it, that's fine with the author, Riddle.
## But if you want to edit the code, comment out the parts you don't want and add
## comments telling where your code was added.
## If you examine the source code and read the comments, it should be easy to use without much headache.
## If you do need help, however, here are contacts for the author:
## email: J.Riddle.x@gmail.com
## aim: J Riddle x
##
##################################################################################################################
##################################################################################################################
 
import md5,sha; from random import choice; from os import access,F_OK

##################################################################################################################
#repeat line generator: prints random replacement lines in a config file, 'cfgfile'
def repgen(cfgfile): #cfgfile= config file to which you want to write the generated replace lines (WILL OVERWRITE)
  num= 0; reps= []
  chars='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%\&\'()*+,-./:;<=>?@[\\]^_`{|}~'
  for num in range(0,len(chars)):
    reps.append('replace %s:%s\n' % (chars[num],chars[choice(range(0,len(chars)))]))
  cfg= file(cfgfile,'w')
  for num in range(0,len(reps)):
    cfg.write(reps[num]); cfg.close
##################################################################################################################

##################################################################################################################
#replacement loop function- does replacements on strob as cfgtxt tells to; return the modified strob
def reploop(strob,cfgtxt): #strob= string object (target of the replacements); cfgtxt= list object with rep lines
  for num in range(0,len(cfgtxt)):
    if cfgtxt[num].startswith('replace '):
      tmpline= cfgtxt[num].strip('replace ')
      strob= strob.replace(tmpline.split(':')[0],tmpline.split(':')[1])
  return strob
##################################################################################################################

##################################################################################################################
#hash generator- either writes the hash to a specified config file, or just returns it (as used by hashcmp())
#if you want to write to the file, the third argument should be 1; the fourth argument should be the hash name

def hashgen(tmppass,cfgfile,*writedata):    #tmppass= password to gen a hash for; cfgfile= config file to use
  if access(cfgfile,F_OK):                  #writedata= tells us if to write, and if so, the hash name
    cfg= file(cfgfile,'r'); cfgtxt= cfg.readlines(); cfg.close()
    tmppass= reploop(tmppass,cfgtxt);
      #coders: if you know what you are doing, you can make the md5/sha hash(es) go through the reploop function too
      #(which would add some extra confusion in any attempt to decrypt the hashes)
    hash= sha.sha(md5.md5(tmppass).hexdigest()).hexdigest()
    if writedata[0]:
      cfg= file(cfgfile,'a'); cfg.write('hash %s %s\n' % (writedata[1],hash)); cfg.close()
    else:
      return hash
###################################################################################################################

###################################################################################################################
#hash comparing function- a function used to compare two hashes
#third argument should be 1 if you want to load a hash from the config file (if so, fourth argument= hash name)
#third argument should be 0 if you want to compare with a hash which you will supply (if so, fourth argument= hash)
#returns 1 if they're the same, returns 0 otherwise

def hashcmp(tmppass,cfgfile,*cmphash):    #tmppass= password to compare the saved password to
  if cmphash[0]:                          #cfgfile= file to generate the hash with
    if access(cfgfile,F_OK):              #         and load the fourth argument, the hash name, from (but only if the third argument= 1)
      cfg= file(cfgfile,'r'); cfgtxt= cfg.readlines(); cfg.close()
      for num in range(0,len(cfgtxt)):
        if cfgtxt[num].startswith('hash %s ' % cmphash[1]):
          if hashgen(tmppass,cfgfile,0,0) == cfgtxt[num].split(cmphash[1]+' ')[1].strip('\n'):
            return 1
      return 0
  else:
    if hashgen(tmppass,cfgfile,0) == cmphash[1]:
      return 1
    else:
      return 0
##################################################################################################################
