###Simple creation, configuration and installation of logging handlers

Originally published: 2010-12-11 08:11:30
Last updated: 2011-06-01 12:13:21
Author: Nick Coghlan

Creation of log message handler for the logging module is often a multi-step process, involving creation of the handler object, configuration of the message levels and formats, installation of any filters and then actual connection of the handler to the relevant logger object.\n\nThis helper function allows all of these things to be specified up front in a single function call, which then takes care of configuring the handler object appropriately.\n\n