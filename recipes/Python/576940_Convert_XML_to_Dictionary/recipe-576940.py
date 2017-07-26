import re
import simplejson as json

def xml2dict(xml, jsonString = ''):
    tags, keys = re.findall('</?[A-Za-z0-9]+>',xml), []
    for tag in tags: keys.append(re.sub('[</>]+','',tag))
    for index in range(len(tags)-1):
        jsonString += {'<><>':   '"'+keys[index]+'": {',
                       '<></>':  '"'+keys[index]+'": "'+xml[xml.find(tags[index])+len(tags[index]):xml.find(tags[index+1])]+'"',
                       '</><>':  ', ',
                       '</></>': '}'}[tags[index].replace(keys[index],'')+tags[index+1].replace(keys[index+1],'')]
    return json.loads('{%s}' % jsonString)
