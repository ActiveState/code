## Android Gmail: export messages from SQLite database blobs

Originally published: 2012-04-17 09:02:42
Last updated: 2013-03-22 11:45:11
Author: ccpizza 

This script will extract email message bodies from the SQLite database stored in an android phone.\n\nThe gmail database is typically located on your phone under the following location:\n\n    `\\data\\data\\com.google.android.gm\\databases\\mailstore.YOURUSERNAME@gmail.com.db`\n\nTo use the script, copy the file above from your phone to your machine and rename it to `gmail.db`.\n\n*NOTE:* You need a rooted phone in order to get access to the folder above.