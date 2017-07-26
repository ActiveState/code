# WebpageTemplate.py: User-friendly template class targeted toward Web-page usage
# and optimized for speed and efficiency.
#
# Copyright (C) 2008-2010  David Gaarenstroom <david.gaarenstroom@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

"""
User friendly template class targeted towards Web-page usage and optimized for 
speed and efficiency.


Tags can be inserted in a template HTML file in a non-intrusive way, by using 
specially formatted comment strings. Therefore the template-file can be viewed 
in a browser, even with prototype data embedded in it, which will later be 
replaced by dynamic content.
Also, webdesigners can continue to work on the template and upload it without 
modification.

For example:
---- template.html ----
<html>
<head><title><!-- start TITLE -->This is a default title<!-- end TITLE --></title></head>
...
---- template.html ----

Load this template using:
>>> template = WebpageTemplate.WebpageTemplate("template.html")
>>> template['TITLE'] = "Try me..."
>>> print str(template)
<html>
<head><title>Try me...</title></head>
...
"""

class WebpageTemplate:
	"""
	Load a template file and substitute tags in it.

	The syntax for the tags is:
	"<!-- start " <tagname> " -->"
		<an optional default string can be placed in between>
	"<!-- end " <tagname> " -->"

	This way a graphics designer can create a working HTML file
	demonstrating what the page should look like, while the dynamic
	content markers do not interfere with this. Code can go back
	and forth between designer and programmer without modifications.

	Templates can be copied into new instances with some tags
	permanently replaced. This way, site-wide tags only have to
	be substituted once, while URL or session specific tags can
	be replaced per copied instance. This saves some extra work when
	serving lots of pages simultaneously.
	"""
	import re
	markup = re.compile(
			r'(?P<starttag>\<!--\s*start\s+(?P<tagname>\w+)\s*--\>)'
			r'(?P<enclosed>.*?)'
			r'(?P<endtag>\<!--\s*end\s+(?P=tagname)\s*--\>)'
			, re.DOTALL|re.IGNORECASE)

	def __init__(self, filename, basetemplate = None, tags = None):
		"""
			filename     --	filename of the template
			basetemplate --	used to copy one instance to another
			tags         --	any predefined tags already known
		"""
		self.strings = basetemplate or []
		self.tags = tags or {}

		if filename:
			filetemplate = open(filename, 'r').read()

			# Iterate over all template tag matches
			startoffset = 0
			for match in self.markup.finditer(filetemplate):
				# Everything from the last match up to this match is
				# regular text
				self.strings.append(\
					filetemplate[startoffset:match.start('starttag')])

				# Retrieve the tagname from the match
				tagname = match.group('tagname')

				# if there a value already defined for this tag, use it.
				# (either the tag is used more than once or this instance
				# was copied from another instance.) Otherwise use the
				# string between starttag and endtag as default value
				if not tagname in self.tags:
					self.tags[tagname] = match.group('enclosed')

				# Add the tagname to the strings list. Every second string
				# is a tagname
				self.strings.append(tagname)
				startoffset = match.end('endtag')

			# Add the remainder as a whole
			self.strings.append(filetemplate[startoffset:])

	def __contains__(self, k):
		return k in self.tags

	def __setitem__(self, k, v):
		if not k in self.tags:
			raise KeyError, k
		self.tags[ k ] = v

	def __getitem__(self, k):
		return self.tags[ k ]

	def __iter__(self):
		"""
		Return a strings iterator for the current template,
		alternating between the static string parts and the current
		tag-values.
		Combined together this is the template content.
		"""
		stringsiter = iter(self.strings)
		yield stringsiter.next()
		while True:
			yield self.tags[stringsiter.next()]
			yield stringsiter.next()

	def __str__(self):
		"""
		Return a string representation of the current template, using
		the current tag-values as replacement text.
		"""
		return ''.join(self.__iter__())

	def publishiter(self, mydict = None):
		"""
		Return an iterator usable to publish the template with its tags
		replaced, and allow for some last minute (stateless) changes.

		Arguments:
			mydict -- optional dictionary with tags:value that
			          do not apply to the template state. In other
			          words, you can supply tag-values with higher
			          precedence than template instance wide
			          defined/implied tags.
		"""
		tags = dict(self.tags)
		if mydict:
		    tags.update(mydict)

		stringsiter = iter(self.strings)
		yield stringsiter.next()
		while True:
			yield tags[stringsiter.next()]
			yield stringsiter.next()

	def publish(self, mydict = None):
		"""
		Publish the template with its tags replaced, and allow for some
		last minute changes. These changes will not be added to the
		instance.

		Arguments:
			mydict -- optional dictionary with tags:value with
			          higher precedence than already supplied tags.
		"""
		return ''.join(self.publishiter(mydict))

	def copy(self, striptags = None):
		"""
		copy WebpageTemplate to a new instance, optionally stripping away
		some tags that no longer should nor will be overwritten.

		Arguments:
			striptags -- optional dictionary, list or tuple containing
			             tags that should be stripped away.
		"""
		if not striptags:
			return self.__class__(None, self.strings[:], dict(self.tags))
		else:
			stringbuf = []
			tags = {}
			previous_string = self.strings[0]

			for index in range(1, len(self.strings), 2):
				tagname = self.strings[index]
				next_string = self.strings[index + 1] or ''
				if tagname in striptags:
					if isinstance(striptags, dict):
						previous_string = previous_string + \
							striptags[tagname] + next_string
					else:
						previous_string = previous_string + \
							self.tags[tagname] + next_string
				else:
					stringbuf.append(previous_string)
					tags[tagname] = self.tags[tagname]
					stringbuf.append(tagname)
					previous_string = next_string

			stringbuf.append(previous_string)

			return self.__class__(None, stringbuf, tags)
