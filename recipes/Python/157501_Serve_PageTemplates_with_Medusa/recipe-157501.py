#! /usr/bin/env python

import cgi
import os
import re

import medusa.script_handler
import medusa.xmlrpc_handler
import medusa.producers

import PageTemplates.PageTemplate
import PageTemplates.Expressions


class MedusaPageTemplate(PageTemplates.PageTemplate.PageTemplate):
    """ MedusaPageTemplate -> PageTemplate type for use by Medusa handlers

        This type constructs a PT context from a Medusa request when
        instantiated.  Instances also read in their content from disk when
        created.  Clients supply the path to the page template file,
        along with the HTTP query string and header data.

        The built-ins that this type provides may differ from the built-ins
        provided by ZopePageTemplates.  Specifically:

        * request - Constructed from the query string and form data if present.

        * here - This mapping may be provided by the client.  Default is empty.

        * root - This mapping may be provided by the client.  Default is empty.

        * user - This mapping may be provided by the client.  Default is empty.

        * container - By default, a custom mapping filled with the results of
        stat and other os module functions.  Clients can specify that this data
        not be made available.

        * modules - Instances reuse PageTemplates.Expressions.SecureModuleImporter
        for importing modules.  The behavior of SecureModuleImporter allows an
        unrestricted import of any module, but in practice, modules sometimes
        cannot be imported.
    """
    modules = PageTemplates.Expressions.SecureModuleImporter

    context_keys = ('template', 'nothing', 'options', 'request', 'modules',
                    'here', 'container', 'root', 'user', )

    stat_keys = ('st_mode', 'st_ino', 'st_dev', 'st_nlink', 'st_uid', 'st_gid',
                 'st_size', 'st_atime', 'st_mtime', 'st_ctime')

    def __init__(self, path, query, header, here={}, options={}, root={},
                 user={}, restricted=0, edit_content_type='text/html'):
        head, tail = os.path.split(path)

        ## these two attributes are so common in PT markup that it would be a
        ## shame to not set them.
        self.id = tail
        self.title = "Page Template '%s'" % (tail, )

        self.here = here
        self.options = options
        self.root = root
        self.template = self
        self.user = user

        ## gather data about the folder that contains this script
        self.container = {}
        if not restricted:
            self.container.update({'is_mount' : os.path.ismount(head),
                                   'is_link' : os.path.islink(head),
                                   'files' : os.listdir(head),
                                   'name' : os.path.split(head)[-1], })
            self.container.update(dict(zip(self.stat_keys, os.stat(head))))

        ## turn a query string and/or form data in the header into a mapping
        self.request = r = {}
        if query:
            if query.startswith('?'):
                query = query[1:]
            r.update(cgi.parse_qs(query, 0, 0))
        if header:
            r.update(cgi.parse_qs(header, 0, 0))
        [r.__setitem__(k, v[0]) for k, v in r.items() if len(v) == 1]

        ## finally, read in the file as a convenience for the client
        self.pt_edit(open(path, 'r').read(), edit_content_type)

    def pt_getContext(self):
        """ redefine pt_getContext() to produce our kind of context """
        return dict([(k, getattr(self, k, None)) for k in self.context_keys])


class pagetemplate_handler_base(medusa.script_handler.script_handler):
    """ pagetemplate_handler_base -> handler that serves up rendered PT files

        This handler type reuses the majority of the behavior defined by
        medusa.script_handler.script_handler.  The 'match' function is the most
        notable of the reused methods.

        The 'handle_request' method defined below mirrors the script_handler
        behavior.  It also allows POST verbs, and uses the collector from
        medusa.xmlrpc_handler to gather POST data.

        Clients should not use this class directly.  Instead, clients should
        instantiate or subclass the two concrete classes defined below,
        pagetemplate_handler and pagetemplate_xml_handler.
    """
    pt_exceptions = (PageTemplates.PageTemplate.PTRuntimeError,
                     PageTemplates.TALES.TALESError,)

    def __init__(self, filesystem):
        ## explicit call to the super; don't want clients to forget to do this
        medusa.script_handler.script_handler.__init__(self, filesystem)

    def handle_request(self, request):
        [path, params, query, fragment] = request.split_uri()

        if not self.filesystem.isfile(path):
            request.error(404)
            return

        self.hits.increment()
        request.script_filename = self.filesystem.translate(path)

        if request.command in ('post', 'put'):
            cl = request.get_header('content-length')
            length = int(cl)
            if not cl:
                request.error(411)
                return
            else:
                col = medusa.xmlrpc_handler.collector(self, request)
                request.collector = col
        elif request.command in ('get', ):
            self.continue_request(None, request)
        else:
            request.error(405)
            return

    def continue_request(self, data, request):
        """ implements the signature expected by xmlrpc_handler.collector """
        path, params, query, fragment = request.split_uri()

        try:
            pt_obj = self.get_pagetemplate(request.script_filename, query, data)
            response = self.render_pagetemplate(request, pt_obj)
        except self.pt_exceptions, ex:
            print '%r' % ex, ex
            response = '<exception>%s</exception>' % (ex, )

        request['Content-Type'] = self.content_type
        request['Content-Length'] = len(response)
        request.push(response)
        request.done()
        return

    def get_pagetemplate(self, filename, query, data):
        """ get_pagetemplate -> return a PT object.  subclasses can override """
        pt = MedusaPageTemplate(filename, query, data)
        return pt

    def render_pagetemplate(self, request, pagetemplate):
        """ render_pagetemplate -> render a PT object.  subclasses can override """
        options = {}
        res = pagetemplate(**options)
        return res

    def __repr__(self):
        return '<page template request handler at %s>' % id(self)

    def status(self):
        return medusa.producers.simple_producer("""
            <li>PageTemplate Handler
                <ul><li><b>Hits:</b> %s</li>
                    <li><b>Exceptions:</b> %s</li>
                </ul>
            </li>""" % (self.hits, self.exceptions, ))


class pagetemplate_handler(pagetemplate_handler_base):
    """ pagetemplate_handler  -> Medusa HTTP handler

        Concrete handler that returns rendered PT markup as HTML. 
    """
    content_type = 'text/html'
    extension = 'pt'
    script_regex = re.compile(r'.*/([^/]+\.%s)' % extension, re.IGNORECASE)


class pagetemplate_xml_handler(pagetemplate_handler_base):
    """ pagetemplate_xml_handler -> Medusa HTTP handler

        Concrete handler that returns rendered PT markup as XML.
    """
    content_type = 'text/xml'
    extension = 'ptx'
    script_regex = re.compile(r'.*/([^/]+\.%s)' % extension, re.IGNORECASE)
