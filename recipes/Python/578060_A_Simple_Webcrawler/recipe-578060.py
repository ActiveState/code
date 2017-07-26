class Tag:
    name = '';
    text = '';
    first_child = 0;
    parent = 0;
    next_sibling = 0;
    closed = 0;
    depth = 0;
    def get_tag_info_str(self):
        c,p,s = 'none','none','none'
        if self.first_child != 0:
            c = self.first_child.name
        if self.parent != 0:
            p = self.parent.name
        if self.next_sibling != 0:
            s = self.next_sibling.name
        return "name = {}, text = {}\nParent = {}, First Child = {}, Next Sibling = {}\nClosed = {}, Depth = {}\n".format(self.name, self.text, p, c, s, self.closed, self.depth)
      
      
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint

class MyHTMLParser(HTMLParser):
    tag_list = []
    depth = 0;
    previous_tag = 'none';
    mode = 'silent';
  
  
    def handle_starttag(self, tag, attrs):
        if self.mode != 'silent':
            print "Start tag:", tag
            for attr in attrs:
                print "     attr:", attr
        self.depth = self.depth + 1
        t = Tag()
        t.name = tag
        t.depth = self.depth
        if self.previous_tag == 'start':
            # current tag is a first child of the last tag
            t.parent = self.tag_list[len(self.tag_list)-1]
            self.tag_list[len(self.tag_list)-1].first_child = t
        elif self.previous_tag == 'end':
            # current tag is next sibling of the last tag
          
            for x in reversed(self.tag_list):
                if x.depth == self.depth:
                    x.next_sibling = t          
                    if t.parent == 0:
                        t.parent = x.parent
                    break
        elif self.previous_tag == 'startend':
            # current tag is the next sibling of the previous tag
            t.parent = self.tag_list[len(self.tag_list)-1].parent
            self.tag_list[len(self.tag_list)-1].next_sibling = t
          
      
        self.tag_list.append(t)  
        self.previous_tag = 'start'
    def handle_endtag(self, tag):
        if self.mode != 'silent':
            print "End tag  :", tag
        for x in reversed(self.tag_list):
            if x.name == tag and x.closed == 0:
                x.closed = 1
                break
        self.depth = self.depth - 1
        self.previous_tag = 'end'
      
    def handle_startendtag(self, tag, attrs):
        if self.mode != 'silent':
            print "Start/End tag  :", tag
            for attr in attrs:
                print "     attr:", attr
        t = Tag()
        self.depth = self.depth + 1
        t.name = tag
        t.depth = self.depth
        t.closed = 1
          
        if self.previous_tag == 'start':
            # current tag is first child of the last tag
            t.parent = self.tag_list[len(self.tag_list)-1]
            self.tag_list[len(self.tag_list)-1].first_child = t
        elif self.previous_tag == 'startend':          
            # current tag is next sibling of last tag
            t.parent = self.tag_list[len(self.tag_list)-1].parent
            self.tag_list[len(self.tag_list)-1].next_sibling = t
        elif self.previous_tag == 'end':          
            # current tag is next sibling of a previous tag of depth = self.depth
            for x in reversed(self.tag_list):
                if x.depth == self.depth:
                    x.next_sibling = t          
                    if t.parent == 0:
                        t.parent = x.parent
                    break
          
        self.tag_list.append(t)  
        self.depth = self.depth - 1
        self.previous_tag = 'startend'
      
      
    def handle_data(self, data):
        if self.mode != 'silent':
            print "Data     :", data
      
        self.depth = self.depth + 1
      
        # add data to last tag in list with depth = current depth - 1
        for x in reversed(self.tag_list):
            if x.depth == self.depth - 1:
                x.text = (x.text + ' ' + data.strip(' \n\t')).strip(' \n\t')
                break
              
        self.depth = self.depth - 1
      
    def handle_comment(self, data):
        if self.mode != 'silent':
            print "Comment  :", data
    def handle_entityref(self, name):
        if self.mode != 'silent':
            c = unichr(name2codepoint[name])
            print "Named ent:", c
    def handle_charref(self, name):
        if self.mode != 'silent':
            if name.startswith('x'):
                c = unichr(int(name[1:], 16))
            else:
                c = unichr(int(name))
            print "Num ent  :", c
    def handle_decl(self, data):
        if self.mode != 'silent':
            print "Decl     :", data
      
    def print_tag_list(self, u):
        for l in self.tag_list:
            print l.get_tag_info_str()
          
    def clear_tag_list(self):
        self.tag_list.__delslice__(0,len(self.tag_list))
    
    def pretty_print_tags(self):
        for t in self.tag_list:
            s = ''
            s = s + self.get_indent_str(t.depth-1)
            s = s + self.get_tag_str(t.name)
            print s

    def get_indent_str(self, n):
        s = ''
        while(n != 0):
            s = s + '    '
            n = n - 1          
        return s
          
    def get_tag_str(self, name):
        return '<{}>'.format(name)
      
    def find_first_tag(self, name):
        r = 0
        for t in self.tag_list:
            if t.name == name:
                r = t
                break
        return r
      
    def print_first_tag_info(self, name):
        t = self.find_first_tag(name)
        if t == 0:
            print "Tag: {} not found".format(name)
        else:
            print t.get_tag_info_str()











import urllib
import socket
socket.setdefaulttimeout(10)
import httplib

class WebCrawler:
    """A simple web crawler"""
      
    link_dict = {};
    initial_depth = 0;
    #filter_list = [];
    parser = 0;
    re_compiled_obj = 0;
    
    class PageInfo:
        """ i store info about a webpage here """
        has_been_scraped = 0;
        word_dict = {};
                 
          
    def __init__(self,re_compiled_obj):      
        #self.filter_list.append(self.Filter(1,'.cnn.'))
        self.parser = MyHTMLParser()
        self.re_compiled_obj = re_compiled_obj
          
    def get_page(self,url):
        """ loads a webpage into a string """
        page = ''
        try:
            f = urllib.urlopen(url=url)
            page = f.read()
            f.close()
        except IOError:
            print "Error opening {}".format(url)
        except httplib.InvalidURL, e:
            print "{} caused an Invalid URL error.".format(url)
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server couldn\'t fulfill the request.'
                print 'Error code: ', e.code        
                
        return page
  
    def check_filters(self,url):
        """ If the url_str matches any of the
        enabled filter strings
        then put the url in the dictionary """
        
        
        match = self.re_compiled_obj.search(url)
        #print "match = {}".format(match)
        return match
  
      
    def find_h1_tag(self,s,pos):
        """ finds the first <h1> tag """
        start = s.find('<h1>',pos)
        end = s.find('</h1>',start)
        return start, end

    def save_tag_text(self, tag, d):
        """ stores each word in the tag in a dictionary """
        if tag != 0:
            token_list = tag.text.split(' ')
            for token in token_list:
                #print 'token = {}'.format(token)
                if d.has_key(token):
                    d[token] = d[token] + 1
                else:
                    d[token] = 1
        return d
      
    def save_page_text(self,page_str):
        """ Save all important text on the page """
        offset = 0
        d = {}
      
        while offset != -1:
            start,end = self.find_h1_tag(page_str,offset)
            offset = end
      
            if start != -1 and end != -1:
                h1_tag = page_str[start:end+5]
                #print h1_tag
                self.parser.clear_tag_list()
                # turn text into linked list of tags
                # only feed part of the page into the parser
                self.parser.feed(h1_tag)                                 
                #self.parser.pretty_print_tags()
                tag = self.parser.find_first_tag('h1')
                # add words from tag into the dictionary
                d = self.save_tag_text(tag,d)
        return d
      
    def save_all_links_on_page(self,page_str,limit=60):
        """ Stores all links found on the current page in a dictionary """
        d = {}
        offset = 0
        i = 0
        num_pages_filtered = 0
        num_duplicate_pages = 0
        while offset != -1:
            if i == limit:
                break
            offset = page_str.find('<a href="http',offset)
            if offset != -1:
                start = page_str.find('"', offset)
                end = page_str.find('"',start+1)
                link = page_str[start+1:end]
                # don't just save all the links
                # filter the links that match specified criteria
                if self.check_filters(link):
                    if link not in self.link_dict:
                        # adding link to global dictionary
                        self.link_dict[link] = self.PageInfo()
                        # adding link to local dictionary
                        d[link] = self.PageInfo()
                    else:
                        num_duplicate_pages = num_duplicate_pages + 1
                else:
                    num_pages_filtered = num_pages_filtered + 1
                offset = offset + 1
            i = i + 1
        print "{} out of {} links were filtered".format(num_pages_filtered,i)
        print "{} out of {} links were duplicates".format(num_duplicate_pages,i)
        #print "{} links are being returned from save_all_links".format(len(d))
        return d
  
  
  
  
    def save_all_links_recursive(self,links,depth):
        """ Recursive function that
            1) converts each page (link) into a string
            2) stores all links found in a dictionary """
        d = {}
      
        print "We are {} levels deep".format(self.initial_depth - depth)
      
        if depth != 0:
            depth = depth - 1
            urls = links.viewkeys()
            #print "There are {} urls".format(len(urls))
            for url in urls:
                print "trying to get {} over the internet".format(url)
                page_str = self.get_page(url)
                print "done getting {} over the internet".format(url)
                self.link_dict[url].word_dict = self.save_page_text(page_str)
                d = self.save_all_links_on_page(page_str)
                self.link_dict[url].has_been_scraped = 1
                # d contains all the links found on the current page
                self.save_all_links_recursive(d,depth)

    def start_crawling(self,seed_pages,depth):
        """ User calls this function to start crawling the web """
        d = {}
        self.link_dict.clear()
       
        # initialize global dictionary variable to the seed page url's passed in
        for page in seed_pages:           
            self.link_dict[page] = self.PageInfo()
            d[page] = self.PageInfo()
        self.initial_depth = depth
        # start a recursive crawl
        # can't pass in self.link_dict because then i get a RuntimeError: dictionary changed size during iteration
        self.save_all_links_recursive(d,depth)
      
    def print_all_page_text(self):
        """ prints contents of all the word dictionaries """
        for i in range(len(self.link_dict)):
            page_info = self.link_dict.values()[i]
            url = self.link_dict.keys()[i]
            print 'url = {}, has_been_scraped = {}'.format(url,page_info.has_been_scraped)
            d = page_info.word_dict
            for j in range(len(d)):
                word = d.keys()[j]
                count = d.values()[j]
                print '{} was found {} times'.format(word,count)
      
import re
                
cnn_url_regex = re.compile('(?<=[.]cnn)[.]com')                


# (?<=[.]cnn)[.]com regular expression does the following:
# 1) match '.com' exactly
# 2) then looking backwards from where '.com' was found it attempts to find '.cnn'


                
w = WebCrawler(cnn_url_regex)
w.start_crawling(['http://www.cnn.com/2012/02/24/world/americas/haiti-pm-resigns/index.html?hpt=hp_t3'],1)
