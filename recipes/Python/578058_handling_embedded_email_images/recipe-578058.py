def make_local_image( embedded_cid , filename, payload):
    """helper func that creates an image object. others may replace this with a specific solution. 
    the important point is that it returns a link 

    """
    import models #my models module. you will probably replace this entire function with your own code
    image_model = models.EmbeddedImageModel(filename=filename,
                                            data = payload)
    image_model.put()
    return image_model.link
    
def cid_2_images(message):
    '''this replaces the <img src="<cid:SOMETHING>"/> tags with <img src="SOME URL"/> tags in the message'''
    from BeautifulSoup import BeautifulSoup 
    import re
    cid_to_link = {}
    for part in message.walk():
        if part.get('Content-ID') :
            logging.info('found cid:%s', part.get('Content-ID'))
            cid_to_link[part.get('Content-ID')] = \
                    make_local_image(part.get('Content-ID'),
                                     part.get_filename(),
                                    part.get_payload(decode=True)
                                     )
    
    for part in message.walk():
        if str(part.get_content_type()) == 'text/html':
            soup = BeautifulSoup(part.get_payload(decode=True))
            images_with_cid = soup('img', attrs = {'src' : re.compile('cid:.*')})            
            for image_tag in images_with_cid:
                cid = '<%s>'% image_tag['src'][4:]
                image_tag['src'] = cid_to_link[cid]
            part.set_payload(soup.renderContents())
