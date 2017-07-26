import re
# set here all chars that needed to be changed 
map = {' ' : '_',
       '.' : '_dot_',
       '&' : '_and_',
       '$' : '_dolar_',
       ':' : '_colon_',
       ',' : '_comma_'
       }

_under = re.compile(r'_+')

def parse_for_beautiful_url(text):
	# if ch does not exists in the map return ch
	str = ''.join([map.get(ch,ch) for ch in text])
	# now we need to clear all types of __ ___ ____ to _ 
	str = _under.sub('_',str)
	# remove the last underscore if exis
	if str[-1:] == '_': return str[0:-1]
	return str
