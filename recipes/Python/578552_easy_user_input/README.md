## easy user input  
Originally published: 2013-06-07 12:45:54  
Last updated: 2013-09-13 06:34:08  
Author: yota   
  
Improvement over Recipe 577058 and cie.

`easy_input()` function extends the built-in `input()` function.
A question is prompted as well as some expected answers.

The user input can be incomplete (ie. `y` or `ye` instead of `yes`)

* If no list of expected answer is provided, default will be "yes/no".
* If no default answer is provided, default will be the first expected answer.

Try and see.

Disclaimer: written in python3, meant for *nix shell, indented with tabs

**Avoided caveat:** If some expected `answer` have the same beginning, the user can not enter too few letters. Ex: `answer = ['continue', 'test', 'testicle']`, user can not input `t`, `te` or `tes` because it will be ambiguous. User can however input `test`, which is not.