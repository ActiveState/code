## Customizing Distutils to Recognize Subversion Committed Revision Numbers

Originally published: 2008-06-08 08:01:04
Last updated: 2008-12-18 14:03:51
Author: Chad Stryker

The script shows how the standard Distutils module can be easily customized to add new features.  In this example, a typical "setup.py" file is configured to extract revision information from a Subversion (revision control repository) database and use the information to set the version of the distribution.