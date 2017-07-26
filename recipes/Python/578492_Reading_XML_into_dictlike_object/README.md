## Reading XML into dict-like object

Originally published: 2013-03-14 02:30:24
Last updated: 2013-03-14 18:50:07
Author: Lucas Oliveira

- Load XML, tree or root\n- Make its children available through __getitem__\n- Make its attributes available through __getattr__\n- If child is requested, return an instance created with child as new root\n- Make its text accessible through __getattr__, using attribute "text"