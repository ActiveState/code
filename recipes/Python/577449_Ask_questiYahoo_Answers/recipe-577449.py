# Use YQL to answer questions with Yahoo! answers and python-yql
# Download Python-YQL from http://python-yql.org
import yql
import sys
import optparse

def prepare_answer(answer):
    attrs = map(answer.get, ['Subject', 'ChosenAnswer', 'Date', 'UserNick', 'ChosenAnswererNick', 'Link'])
    prefixes = ('Question', 'Answer', 'Answered On', 'Asked By', 'Answered By', 'Link')
    lines = []

    for x in range(len(attrs)):
        val = attrs[x]
        if val != None:
            lines.append(': '.join((prefixes[x].ljust(15), val)))

    return '\n'.join(lines)
    
def fetch_answer(*question, **kwargs):
    query="select * from answers.search where query='%s'"
    y = yql.Public()
    print 'You asked: ',' '.join(*question)
    result = y.execute(query % ' '.join(*question))

    if len(result.rows)==0:
        print 'No answers found!'
        return

    limit = kwargs['limit']
    
    if limit>0:
        results = result.rows[:limit]
    else:
        results = result.rows
        
    for item in results:
        if item.get('type')==u'Answered':
            print prepare_answer(item)
            print '_'*82
            
if __name__ == "__main__":
    if len(sys.argv)<2:
        sys.argv.append('-h')
        
    parser = optparse.OptionParser()
    parser.add_option('-n','--num',type=int,dest='nresults',default=0,help='Maximum number of results')
    options, args = parser.parse_args()
    nresults = options.__dict__['nresults']
    
    fetch_answer(args, limit=nresults)
