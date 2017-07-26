import urllib2
from BeautifulSoup import BeautifulSoup
import webbrowser

# Remote Path to your Wikimedia instalation
remote_link = ""

# Special link for Wikimedia to the Recent Changes Special Page
recent_changes_link = "index.php/Special:RecentChanges"

link = remote_link + recent_changes_link

page = urllib2.urlopen(link)

soup = BeautifulSoup(page)

test = soup.findAll(text=u"diff")

if len(test) != 0:
    webbrowser.open(link)
