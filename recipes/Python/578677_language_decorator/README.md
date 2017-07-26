## language decorator

Originally published: 2013-10-02 07:59:03
Last updated: 2013-10-02 08:00:29
Author: Dr. Trigon

Use other languages like lua, C++ or simple bash from python. Instead of writing code as a string and then send it to some eval or execute function, we introduce here decorators that allow to write regular python functions containing the external code as docstring.\n\nThat way the external code needs minimal adoptions only and becomes better read- and maintainable. Write your function in your favourite language and just place the right decorator in front of it - it simple like that.\n\nAt the current state this recipe is a DRAFT and needs to be further extended and tested.