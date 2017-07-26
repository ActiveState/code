## An ActiveRecord like ORM (object relation mapper) under 200 linesOriginally published: 2006-07-24 23:31:23 
Last updated: 2006-07-26 16:49:55 
Author: Wensheng Wang 
 
There're quite a few python ORM's. However, most are not easy to use.  In Ruby on Rails's ActiveRecord ORM, you don't have to define schema, just specify the relationship like "belongs_to" and "has_many", and ORM do rest of the work, it's very easy to learn and easy to use.\nThis recipe provide a python ORM that behave like ActiveRecord.