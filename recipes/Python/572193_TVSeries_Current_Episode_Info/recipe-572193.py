# TV-Series Current Episode Info 1.02
# Date: 2008/05/08
# License: As-is; public domain
# Prerequisites: Python 2.5.2, IMDbPY 3.5

# Description: The getEps function in this module returns a text string containing the original air date for the last aired and next upcoming episodes of a TV series title. It also provides the plot for the next upcoming episode, if available. The information returned is limited to what is available at IMDb, and so it may not be up to date. IMDbPY (http://imdbpy.sourceforge.net/) is used. It is designed especially for use by an IRC or other text bot.

# Usage:
# from getEps import getEps
# getEps('title of a TV series')

# Usage examples:
# getEps('terminator')
# The episode that aired last for "Terminator: The Sarah Connor Chronicles" (2008) is "The Demon Hand" (S01E07). It aired 4 days ago, i.e. on Mon, 25 Feb 08. The next upcoming episode is "Vick's Chip" (S01E08). It airs in 3 days, i.e. on Mon, 3 Mar 08. Its plot is unavailable.
# getEps('smallville')
# The episode that aired last for "Smallville" (2001) is "Fracture" (S07E12). It aired 15 days ago, i.e. on Thu, 14 Feb 08. The next upcoming episode is "Hero" (S07E13). It airs in 13 days, i.e. on Thu, 13 Mar 08. Its plot is: Pete Ross returns to Smallville and finds a number of surprising changes since his departure four years earlier. Besides resolving his feelings toward Clark since he learned of his friend's secret, Pete has to deal with the acquisition of a superpower of his own.
# getEps('stargate atlantis /noplot')
# The episode that aired last for "Stargate: Atlantis" (2004) is "The Kindred: Part 1" (S04E18). It aired 7 days ago, i.e. on Fri, 22 Feb 08. The next upcoming episode is "The Kindred: Part 2" (S04E19). It airs today, i.e. on Fri, 29 Feb 08.

# Keywords:
# tv, television, tv show, tv series, tv episodes, episodes, 
# last episode, previous episode, next episode, upcoming episode, future episode, 
# episode date, episode air date, episode schedule, original air date, 
# imdb, imdbpy, 
# tv bot, tv show bot, tv episode bot

# Import needed modules and methods
from imdb import IMDb
from imdb.helpers import sortedEpisodes
from itertools import dropwhile, ifilter, islice, takewhile
from datetime import date
from time import sleep, strptime
import locale

# Set locale
locale.setlocale(locale.LC_ALL,'') # This is used for formatting numbers

def getEps(title,max_len=990,debug=False): # 1024-32-2 = 990
	"""Returns a text string containing schedule info for the last aired and the next upcoming episodes for the given TV series title"""

	# Validate title
	assert isinstance(title,str), 'A string input was not provided.'

	# Preprocess title
	title=title.strip()

	# Determine if the next upcoming episode's plot should be included if available (Default is True)
	if title.lower().endswith('/noplot'):
		title=title[:-len('/noplot')].rstrip()
		include_plot=False
	else:
		include_plot=True

	try:

		# Validate title further
		if len(title)==0: return 'A title was not provided.'
	
		# Create IMDb object
		i=IMDb()
	
		# Get search results
		max_attempts=3 # Set to anything greater than 1
		for attempt in range(1,max_attempts+1):
			try:
				search_results=i.search_movie(title)
				break
			except:
				if attempt<max_attempts:
					if debug: print 'An error occurred while attempting to retrieve search results for "%s". %s attempts were made.'%(title,attempt)+'\n'
					sleep(attempt*2)
				else:
					return 'An error occurred while attempting to retrieve search results for "%s". %s attempts were made.'%(title,attempt)
		del attempt,max_attempts
	
		# Get first search result that is a TV series
		search_results=ifilter(lambda s:s['kind']=='tv series',search_results)
		search_results=list(islice(search_results,0,1))
		if len(search_results)==0: return 'No TV series matches were found for "%s".'%title
		s=search_results[0]
		del search_results
	
		# Get episodes
		i.update(s,'episodes')
		s_title=s['long imdb title']
		if (not s.has_key('episodes')) or len(s['episodes'])==0: return 'Episode info is unavailable for %s.'%s_title
		s=sortedEpisodes(s)
		if len(s)==0: return 'Episode info is unavailable for %s.'%s_title
	
		# Sort episodes in approximately the desired order
		s.reverse() # This results in episodes that are sorted in the desired order. If, however, the episodes are not listed in proper order at the source, such as for "Showtime Championship Boxing" (1987) as of 2/29/08, the error will be copied here.
		s=list(dropwhile(lambda e:e['season']=='unknown',s))+list(takewhile(lambda e:e['season']=='unknown',s)) # While this may not always produce the most accurate results, it prevents episodes belonging to an unknown season from being thought of as most recent.
	
		# Process date related info for episodes
		date_today=date.today()
		for ep_ind in xrange(len(s)):
			if s[ep_ind].has_key('original air date'):
				try:
					s[ep_ind]['date']=strptime(s[ep_ind]['original air date'],'%d %B %Y')
				except:	pass
			if s[ep_ind].has_key('date'):
				s[ep_ind]['date']=date(*s[ep_ind]['date'][0:3])
				s[ep_ind]['age']=(s[ep_ind]['date']-date_today).days # Age is date delta in days
				if s[ep_ind]['age']<0:
					s[ep_ind]['has aired']=True
				else:
					s[ep_ind]['has aired']=False
			else:
				s[ep_ind]['has aired']=False
		del date_today,ep_ind
	
		# Print last 10 listed episodes (if debugging)
		if debug:
			print 'Last 10 listed episodes:\nS# Epi# Age   Episode Title'
			for e in s[:10]: print '%s %s %s %s'%(str(e['season']).zfill(2)[:2],str(e['episode']).zfill(4),e.has_key('age') and str(e['age']).zfill(5) or ' '*5,e['title'].encode('latin-1'))
			print
	
		# Declare convenient functions for use in generating output string
		def getSE(e):
			if not isinstance(e['season'],int): return ''
			Sstr='S'+str(e['season']).zfill(2)
			Estr='E'+str(e['episode']).zfill(2)
			return ' ('+Sstr+Estr+')'
		def getAge(e): return locale.format('%i',abs(e['age']),grouping=True)
		def getDate(e): return 'i.e. on '+e['date'].strftime('%a, ')+str(e['date'].day)+e['date'].strftime(' %b %y')
	
		# Determine last aired episode
		# (An episode that airs today is considered to be not yet aired)
		e=ifilter(lambda e:e['has aired'],s)
		e=list(islice(e,0,1))
		if len(e)>0:
			e=e[0]
			e_schedule= e['age']!=-1 and ('%s days ago'%getAge(e)) or 'yesterday'
	
			# Generate output string when last aired episode is available
			e_out='The episode that aired last for '+s_title+' is "'+e['title']+'"'+getSE(e)+'. It aired '+e_schedule+', '+getDate(e)+'. '
			del e_schedule
	
		else:
			# Generate output string when last aired episode is unavailable
			e_out=''
	
		# Determine next upcoming episode
		# (An episode that airs today is considered to be an upcoming episode)
		e=list(takewhile(lambda e:e['has aired']==False,s)) # Memory inefficient
		if len(e)>0:
			e=e[-1]
	
			# Generate output string when next upcoming episode is available
			e_out=e_out+'The next upcoming episode '+(e_out=='' and ('for '+s_title+' ') or '')+'is "'+e['title']+'"'+getSE(e)+'.'
	
			if e.has_key('age'):
				e_schedule= e['age']>1 and ('in %s days'%getAge(e)) or e['age']==1 and 'tomorrow' or e['age']==0 and 'today'
				e_out=e_out+' It airs '+e_schedule+', '+getDate(e)+'.'
				del e_schedule
			else:
				e_out=e_out+' Its air date is unavailable.'
	
			if include_plot:
				if e.has_key('plot') and e['plot']!='Related Links':
					e_out=e_out+' Its plot is: '+e['plot']
				elif e_out.endswith('Its air date is unavailable.'):
					e_out=e_out.replace('Its air date is unavailable.','Its air date and plot are unavailable.')
				else:
					e_out=e_out+' Its plot is unavailable.'
	
		else:
			if e_out!='': # Last: available; Next: unavailable
				e_out=e_out+'No upcoming episode is scheduled.'
			else: # Last: unavailable; Next: unavailable
				e_out='Episode info is unavailable for %s.'%s_title
	
		# Conditionally trim output string
		if (max_len not in [-1,0,None]) and len(e_out)>max_len-3: e_out=e_out[:max_len-3]+'...'
	
		# Return output string
		return e_out

	except:	return 'An error occurred while attempting to retrieve episode info for "%s".'%title

def getEps_test(add_noplot=False):
	"""Run a set of tests"""

	# Make a tuple of sample titles in alphabetical order
	titles=('24', # As of 2/21/08, this item has inconsistent schedule info
		'arrested development',
		'avatar',
		'big brother',
		'dexter',
		'future weapons', # As of 2/21/08, this item has inconsistent schedule info
		'heroes',
		'kid nation',
		'kyle xy',
		'las vegas',
		'lost',
		'my name is earl',
		'nip tuck',
		'numbers', # This item is a misspelled name of a TV series and it has an unaired pilot
		'prison break',
		'scrubs',
		'showtime championship boxing', # The episodes for this item are not correctly sorted by date
		'smallville',
		'south park',
		'stargate atlantis',
		'stargate sg1', # This item doesn't have an upcoming episode
		'supernatural',
		'terminator', # This item is a partial name of a TV series
		'the daily show', # All episodes for this item belong to an unknown season
		'the oc',
		'the office',
		'the universe',
		'the wire',
		'twilight zone',
		'ufo hunters',
		'weeds',
		'zzkjsdfglkjfsdg') # This item does not correspond to any TV series

	#titles=('',) # For testing a single or limited number of TV-series

	for title in titles:
		print title+':\n'
		print getEps(title,debug=True)+'\n'+'_'*72+'\n'
		if add_noplot:
			print title+': '+getEps(title+' /noplot',debug=True)++'\n''_'*72+'\n'

# Run tests
if __name__=='__main__': getEps_test()
