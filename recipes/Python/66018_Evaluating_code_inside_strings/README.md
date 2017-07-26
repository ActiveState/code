## Evaluating code inside strings  
Originally published: 2001-07-12 00:45:34  
Last updated: 2001-07-12 00:45:34  
Author: Joonas Paalasmaa  
  
In Python, String and Unicode objects have one special operator: the % operator.
With that operator, strings can be formatted with format codes.
Formatting is given syntax format % values, where format is a string with format codes that are replaced with values.
When value is any kind of mapping, formats must include parenthesis that contain a key.
An item is fetched from directory with key or __getitem__ is overloaded with key.
In this example, Eval's __getitem__ returns the result of eval(key).