## A SAX filter for normalizing text eventsOriginally published: 2004-01-14 17:00:10 
Last updated: 2005-04-10 06:06:10 
Author: Uche Ogbuji 
 
A SAX parser can report contiguous text using multiple characters events.  This is often unexpected and can cause obscure bugs or require complicated adjustments to SAX handlers.  By inserting text_normalize_filter into the SAX handler chain all downstream parsers are ensured that all text nodes in the document Infoset are reported as a single SAX characters event.