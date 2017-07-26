From DTML:

<dtml-call "RESPONSE.setHeader('Cache-Control', 'no-cache')">
<dtml-call "RESPONSE.setHeader('Pragma', 'no-cache')">


From python/python script:

def noCache(self, REQUEST):
    REQUEST.RESPONSE.setHeader('Cache-Control', 'no-cache')
    REQUEST.RESPONSE.setHeader('Pragma', 'no-cache')
