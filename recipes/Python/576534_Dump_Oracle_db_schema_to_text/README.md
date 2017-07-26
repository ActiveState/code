## Dump Oracle db schema to text 
Originally published: 2008-10-10 05:34:02 
Last updated: 2014-02-21 09:18:55 
Author: Michal Niklas 
 
Export Oracle schema to text.\nUsable to compare databases that should be the same\n\nOracle schema info:\nhttp://www.eveandersson.com/writing/data-model-reverse-engineering\n\nWith `--separate-files` can save table information as `CREATE TABLE` statements and all view/function art objects are in separate files (sometime it is easier to compare directories with files than compare two big files)\n