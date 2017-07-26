## Mapping arbitrary objects to a PostgreSQL database with psycopg2Originally published: 2004-09-10 12:17:53 
Last updated: 2004-09-10 12:17:53 
Author: Valentino Volonghi 
 
You need to store arbitrary objects in a PostgreSQL database without being\nintrusive for your classes (don't want inheritance from an 'Item' or\n'Persistent' object).