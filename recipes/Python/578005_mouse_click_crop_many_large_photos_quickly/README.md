## mouse click to crop many large photos quickly [Python, PIL, pygame]

Originally published: 2012-01-09 03:18:01
Last updated: 2012-01-09 03:18:01
Author: Elliot Hallmark

Waste no mouse clicks making multiple crops on many image files.  Through pygame interface with pan, zoom and next/previous image.  Saves files at new resolution and serialized names in a seperate folder.  the mainloop() and helper functions are easy to reuse, but I include a cruddy text based interface if needed.  if not, comment out most of __main__().\n\nRequires PIL (python imaging library) and pygame.\n