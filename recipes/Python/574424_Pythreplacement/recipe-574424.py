#! /usr/bin/env python
"""
A Python replacement for java.util.Properties class

Handles Unicode escapes
Preserves comments and order of lines

Created - Anand B Pillai <abpillai@gmail.com>
Updated - Adam Feuer <xxx at pobox.com> (replace xxx with adamf)
"""

import sys,os,codecs
import re
import time

class Properties(object):
   """ A Python replacement for java.util.Properties """
   
   def __init__(self, props=None):
      self._propertyEntries = {}
      self._commentEntries = []
      self.equalOrColonSeparatorWithoutBackslashesRe = re.compile(r'(?<!\\)(\s*\=)|(?<!\\)(\s*\:)')
       
   def loadFromString(self, input):
      lines = input.split('\n')
      self._parse(lines)
       
   def load(self, file):
      """Load properties from an open file stream"""
      unicodeFile = codecs.EncodedFile(file, 'latin-1')
      try:
         lines = unicodeFile.readlines()
         unicodeFile.close()
      except IOError, e:
         raise
      self._parse(lines)

   def getProperty(self, key):
      if self._propertyEntries.has_key(key):
         return self._propertyEntries.get(key)["value"]
      else:
         return ''

   def setProperty(self, key, value):
      if type(key) is str and type(value) is str:
         self._processPair(key, value)
      else:
         raise TypeError,'both key and value should be strings!'

   def propertyNames(self):
      return self._propertyEntries.keys()

   def getAsString(self):
      result = ""
      entries = self._propertyEntries.values() + self._commentEntries
      entries.sort()
      for entry in entries:
         if entry["comment"]:
            result += "%s\n" % entry["line"]
         else:
            result += ''.join((entry["key"],'=',entry["value"],'\n'))
      return result

   def store(self, outFile, header=""):
      self._store(outfile, header)
      outFile.close()

   def _store(self, outFile, header=""):
      unicodeOutFile = codecs.EncodedFile(outFile, 'latin-1')
      unicodeOutFile.write(header)
      unicodeOutFile.write(self.getAsString())

   def getPropertyDict(self):
      propertyDict = {}
      for key, entry in self._propertyEntries.items():
         propertyDict[key] = entry["value"]
      return propertyDict

   def __str__(self):
      s='{'
      for key,entry in self._propertyEntries.items():
         s = ''.join((s,key,'=',entry["value"],', '))
      s=''.join((s[:-2],'}'))
      return s

   def __getitem__(self, name):
      """ To support direct dictionary-like access """
      return self._propertyEntries[name]["value"]

   def __setitem__(self, name, value):
      """ To support direct dictionary-like access """
      self._processPair(name, value)
             
   def __getattr__(self, name):
      """For attributes not found in self, redirect
      to the properties dictionary """
      try:
         return self.__dict__[name]
      except KeyError:
         if hasattr(self._propertyEntries, name):
            return getattr(self._propertyEntries, name)
         else:
            raise AttributeError(name)

   def _parse(self, lines):
      lineIterator = iter(lines)
      self.lineNumber = 0
      for line in lineIterator:
         line = line.strip()
         if not line or self._isCommentLine(line):
            self._commentEntries.append(self._getPropertyEntry(comment=True, line=line))
         else:
            indexOfFirstSeparationChar = self._getIndexOfFirstSeparationChar(line)
            line = self._joinLinesIfNecessary(line, lineIterator)
            key, value = self._splitOnSeparationChar(line, indexOfFirstSeparationChar)
            self._processPair(key, value, line)

   def _processPair(self, key, value, line=''):
      origValue = value
      key, origKey = self._removeWhitespaceFromEndOfKey(key)
      origValue = self._unescape(origValue)
      value = self._unescape(value).strip()
      entry = self._getPropertyEntry(key=key, origKey=origKey, value=value, line=line, comment=False)
      self._propertyEntries[key] = entry

   def _getPropertyEntry(self, **kwargs):
      kwargs["lineNumber"] = self.lineNumber
      self.lineNumber += 1
      return PropertyEntry(**kwargs)
       
   def _getIndexOfFirstSeparationChar(self, line):
      indexOfFirstSeparationChar = -1
      endPos = self._getEndPositionOfSearch(line)
      whiteSpaceSeparatorRe = self._getWhiteSpaceSeparatorRe(line)
      if whiteSpaceSeparatorRe.search(line, 0, endPos):
         first, last = whiteSpaceSeparatorRe.search(line, 0, endPos).span()
         indexOfFirstSeparationChar = first
      elif self.equalOrColonSeparatorWithoutBackslashesRe.search(line):
         first, last = self.equalOrColonSeparatorWithoutBackslashesRe.search(line).span()
         indexOfFirstSeparationChar = last - 1
      return indexOfFirstSeparationChar

   def _getEndPositionOfSearch(self, line):
      matchObj = self.equalOrColonSeparatorWithoutBackslashesRe.search(line)
      if matchObj:
         first, last = matchObj.span()
         return first
      else:
         return len(line)
           
   def _getWhiteSpaceSeparatorRe(self, line):
      whiteSpaceSeparatorRe = re.compile(r'(?<![\\\=\:])(\s)')
      if not self.equalOrColonSeparatorWithoutBackslashesRe.search(line):
        self.equalOrColonSeparatorRe = re.compile(r'(\s*\=)|(\s*\:)')
        if self.equalOrColonSeparatorRe.search(line):
           whiteSpaceSeparatorRe = re.compile(r'(?<![\\])(\s)')
      return whiteSpaceSeparatorRe
           
   def _joinLinesIfNecessary(self, line, lineIterator):
      while line[-1] == '\\':
         nextline = lineIterator.next()
         nextline = nextline.strip()
         line = line[:-1] + nextline
      return line

   def _splitOnSeparationChar(self, line, indexOfFirstSeparationChar):
      if indexOfFirstSeparationChar != -1:
         return line[:indexOfFirstSeparationChar], line[indexOfFirstSeparationChar+1:]
      else:
         return line,''

   def _removeWhitespaceFromEndOfKey(self, key):
      origKey = key
      whitespaceAtEndOfKeyRe = re.compile(r'\\(?!\s$)')
      keyparts = whitespaceAtEndOfKeyRe.split(key)
      lastpart = keyparts[-1]
      if lastpart.find('\\ ') != -1:
         keyparts[-1] = lastpart.replace('\\','')
      key = ''.join(keyparts)
      if lastpart and lastpart[-1] == ' ':
         origKey = origKey.strip()
         key = key.strip()
      return key, origKey
   
   def _escape(self, value):
      newvalue = value.replace(':','\:')
      newvalue = newvalue.replace('=','\=')
      return newvalue

   def _unescape(self, value):
      newvalue = value.replace('\:',':')
      newvalue = newvalue.replace('\=','=')
      return newvalue    

   def _isCommentLine(self, line):
      if line[0] == '#': return True
      if line[0] == '!': return True
      return False
        
class PropertyEntry(dict):
   def __init__(self, **kwargs):
      if kwargs is None:
         kwargs = {}
      dict.__init__(self, kwargs)

   def __cmp__(self, other):
      return self.getLineNumber() - other.getLineNumber() 

   def getLineNumber(self):
      return self.get("lineNumber", -1)
