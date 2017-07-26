## LazyDB  
Originally published: 2001-07-25 10:43:12  
Last updated: 2001-07-25 10:43:12  
Author: John Dell'Aquila  
  
LazyDB extends the DB API to provide lazy connections (only\nestablished when needed) and access to query results by column\nname. A LazyDB connection can transparently replace any normal\nDB API connection but is significantly more convenient, making\nSQL queries feel almost like a built-in Python feature.