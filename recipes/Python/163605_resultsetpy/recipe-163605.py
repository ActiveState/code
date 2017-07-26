#!/usr/bin/python

# Wraps DB-API 2.0 query results to provide a nice list and dictionary interface.
# Copyright (C) 2002  Dr. Conan C. Albrecht <conan_albrecht@byu.edu>
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
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


# I created this class and related functions because I like accessing
# database results by field name rather than field number.  Accessing
# by field number has many problems: code is less readable, code gets
# broken when field positions change or fields are added or deleted from
# the query, etc.
# 
# This class should have little overhead if you are already using fetchall().  
# It wraps each result row in a ResultRow class which allows you to 
# retrieve results via a dictionary interface (by column name).  The regular
# list interface (by column number) is also provided.
# 
# I can't believe the DB-API 2.0 api didn't include dictionary-style results.
# I'd love to see the reasoning behind not requiring them of database connection
# classes.

def runquery(cursor, sql):
  """Returns a list of ResultRow objects based upon a connected cursor
     and a query sql string to execute"""
  
  # run the query
  cursor.execute(sql)
  
  # return the list
  return getdict(cursor.fetchall(), cursor.description)
  
  
def getdict(results, description):
  """Returns a list of ResultRow objects based upon already retrieved results 
     and the query description returned from cursor.description"""
 
  # get the field names
  fields = {}
  for i in range(len(description)):
    fields[description[i][0]] = i

  # generate the list of ResultRow objects
  rows = []
  for result in results:
    rows.append(ResultRow(result, fields))

  # return to the user
  return rows

  
class ResultRow:
  """A single row in a result set with a dictionary-style and list-style interface"""
  
  def __init__(self, row, fields):
    """Called by ResultSet function.  Don't call directly"""
    self.row = row
    self.fields = fields
    
  def __str__(self):
    """Returns a string representation"""
    return str(self.row)
    
  def __getitem__(self, key):
    """Returns the value of the named column"""
    if type(key) == type(1): # if a number
      return self.row[key]
    else:  # a field name
      return self.row[self.fields[key]]
    
  def __setitem__(self, key, value):
    """Not used in this implementation"""
    raise TypeError, "can't set an item of a result set"
    
  def __getslice__(self, i, j):
    """Returns the value of the numbered column"""
    return self.row[i: j]
  
  def __setslice__(self, i, j, list):
    """Not used in this implementation"""
    raise TypeError, "can't set an item of a result set"
    
  def keys(self):
    """Returns the field names"""
    return self.fields.keys()
    
  def keymappings(self):
    """Returns a dictionary of the keys and their indices in the row"""
    return self.fields
    
  def has_key(self, key):
    """Returns whether the given key is valid"""
    return self.fields.has_key(key)
    
  def __len__(self):
    """Returns how many columns are in this row"""
    return len(self.row)
    
  
