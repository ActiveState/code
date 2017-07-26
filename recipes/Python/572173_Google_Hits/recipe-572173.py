# Google Hits 1.01
# Date: 2008/06/08
# License: As-is; public domain
# Prerequisites: Python 2.5.2

# Description:
# The getHits function in this file takes as input a search term string, and returns as output a dict containing the number of web hits returned for that search term. The Google search engine and a SQLite database are used.
# The optional input arguments are:
#  - cond_enc (bool) (default is False): enclose the search term in quotes if it contains more than one word
#  - db_name (default is 'Hits.sqlite'): the name of the database to use for caching hits
#  - max_age (default is 30): the maximum acceptable age in days of cached hits

# Usage:
# from getHits import getHits
# hits=getHits('sample search term')['hits']

# Keywords:
# hits, count, popularity
# web search hits, web hits, Google hits

# Import needed modules
import datetime, os.path, re, sqlite3, urllib2

def getHits(term,cond_enc=False,db_name='Hits.sqlite',max_age=30):
    """Get web search hits for a given term"""

    # Validate term
    assert (isinstance(term,str) or isinstance(term,unicode)), 'Term must be a string'

    def getHitsDb(term,con,max_age):
        """Get web search hits for a given term from a database if available"""

        # Get hits from database if available
        row=con.execute('SELECT Hits,DateTimeUTC FROM Hits WHERE Term=?', (hits['term'],)).fetchone()

        # Determine hits from database as available
        if row==None:
            hits['inDb']=False
        else:

            # Postprocess row
            row={'Hits':row['Hits'], 'DateTimeUTC':row['DateTimeUTC']}
            row['DateTimeUTC']=datetime.datetime.strptime(row['DateTimeUTC'],'%Y-%m-%d %H:%M:%S')
            row['Age']=datetime.datetime.utcnow()-row['DateTimeUTC']
            row['Age']=row['Age'].days+row['Age'].seconds/float(datetime.timedelta.max.seconds)

            # Conditionally determine hits based on age of hits
            if row['Age']>max_age:
                con.execute('DELETE FROM Hits WHERE Term=?', (hits['term'],))
                hits['inDb']=False
            else:
                hits['inDb']=True
                hits['hits']=row['Hits']

        # Return updated hits
        return hits

    def getHitsWeb(hits):
        """Get web search hits for a given term from a web search"""

        # Set parameters
        url='http://google.com/search?' # Set web search URL

        # Generate web search term
        hits['web search term']=urllib2.quote(hits['term'])

        # Execute web search
        url=urllib2.Request('%sq=%s'%(url,hits['web search term']))
        url.add_header('User-Agent','')
        url=urllib2.urlopen(url).read()

        # Store date and time of web search
        hits['datetimeutc']=datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        # Parse web search results to determine hits
        hits['hits']=re.search('Results <b>1</b> - <b>10</b> of about <b>(?P<hits>.+?)</b> for <b>',url)
        if hits['hits']!=None:
            hits['hits']=hits['hits'].group('hits')
            hits['hits']=hits['hits'].replace(',','')
            hits['hits']=int(hits['hits'])
        else:
            hits['hits']=0

        # Return updated hits
        return hits

    def setHitsDb(con,hits):
        """Store web search hits for a given term in the database"""
        con.execute('INSERT INTO Hits (Term,Hits,DateTimeUTC) VALUES (?,?,?)', (hits['term'],hits['hits'],hits['datetimeutc']))

    def createDb(db_name):
        """Create a database to store web search hits"""
        con=sqlite3.connect(db_name,isolation_level=None)
        con.execute("""CREATE TABLE `Hits` (`Term` CHAR PRIMARY KEY  NOT NULL , `Hits` INTEGER NOT NULL , `DateTimeUTC` DATETIME NOT NULL )""")

    # Create database if not created
    if not os.path.isfile(db_name): createDb(db_name)

    # Initialize database
    con=sqlite3.connect(db_name,isolation_level=None)
    con.row_factory=sqlite3.Row

    # Create dict to store relevant info
    hits={'term':term}

    # Condtionally enclose term in quotes
    if cond_enc and hits['term'].__contains__(' '): hits['term']='"%s"'%hits['term']

    # Get hits
    hits=getHitsDb(hits,con,max_age) # Get hits from database if available
    if not hits['inDb']:
        hits=getHitsWeb(hits) # Get hits from web
        setHitsDb(con,hits) # Store hits in database

    # Return hits
    return hits

def cleanDb(db_name='Hits.sqlite',max_age=30):
    """Delete entries from database that are older than the specified maximum age in days"""

    # Determine threshold for date and time for old entries
    min_datetime=datetime.datetime.utcnow()-datetime.timedelta(days=30)
    min_datetime=min_datetime.strftime('%Y-%m-%d %H:%M:%S')

    # Delete old entries from database
    con=sqlite3.connect(db_name,isolation_level=None)
    con.execute('DELETE FROM Hits WHERE DateTimeUTC<?', (min_datetime,))
