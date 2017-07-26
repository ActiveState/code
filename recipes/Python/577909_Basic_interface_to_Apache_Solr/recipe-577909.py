"""Simple model of Apache Solr 1.4 and 3.x"""

import json
import urllib
import urllib2

import lxml.etree as etree


class Solr(object):
    """Thin abstraction layer around Apache Solr"""

    def __init__(self, url):
        self.url = url

    def select(self, params):
        """Search Solr, return URL and JSON response."""
        params['wt'] = 'json'
        url = self.url + '/select?' + urllib.urlencode(params)
        conn = urllib2.urlopen(url)
        return url, json.load(conn)

    def delete(self, query, commit=False):
        """Delete documents matching `query` from Solr, return (URL, status)"""
        params = {}
        if commit:
            params['commit'] = 'true'
        url = self.url + '/update?' + urllib.urlencode(params)
        request = urllib2.Request(url)
        request.add_header('Content-Type', 'text/xml; charset=utf-8')
        request.add_data('<delete><query>{0}</query></delete>'.format(query))
        response = urllib2.urlopen(request).read()
        status = etree.XML(response).findtext('lst/int')
        return url, status

    def update(self, docs, commitwithin=None):
        """Post list of docs to Solr, return URL and status.
        Opptionall tell Solr to "commitwithin" that many milliseconds."""
        url = self.url + '/update'
        add_xml = etree.Element('add')
        if commitwithin is not None:
            add_xml.set('commitWithin', str(commitwithin))
        for doc in docs:
            xdoc = etree.SubElement(add_xml, 'doc')
            for key, value in doc.iteritems():
                if value:
                    field = etree.Element('field', name=key)
                    field.text = (value if isinstance(value, unicode)
                                  else str(value))
                    xdoc.append(field)
        request = urllib2.Request(url)
        request.add_header('Content-Type', 'text/xml; charset=utf-8')
        request.add_data(etree.tostring(add_xml, pretty_print=True))
        response = urllib2.urlopen(request).read()
        status = etree.XML(response).findtext('lst/int')
        return url, status

    def commit(self, waitsearcher=False, waitflush=False):
        """Commit uncommitted changes to Solr immediately, without waiting."""
        commit_xml = etree.Element('commit')
        commit_xml.set('waitFlush', str(waitflush))
        commit_xml.set('waitSearcher', str(waitsearcher))
        url = self.url + '/update'
        request = urllib2.Request(url)
        request.add_header('Content-Type', 'text/xml; charset=utf-8')
        request.add_data(etree.tostring(commit_xml, pretty_print=True))
        response = urllib2.urlopen(request).read()
        status = etree.XML(response).findtext('lst/int')
        return url, status
