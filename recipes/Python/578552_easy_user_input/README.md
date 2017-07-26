###easy user input

Originally published: 2013-06-07 12:45:54
Last updated: 2013-09-13 06:34:08
Author: yota 

Improvement over Recipe 577058 and cie.\n\n`easy_input()` function extends the built-in `input()` function.\nA question is prompted as well as some expected answers.\n\nThe user input can be incomplete (ie. `y` or `ye` instead of `yes`)\n\n* If no list of expected answer is provided, default will be "yes/no".\n* If no default answer is provided, default will be the first expected answer.\n\nTry and see.\n\nDisclaimer: written in python3, meant for *nix shell, indented with tabs\n\n**Avoided caveat:** If some expected `answer` have the same beginning, the user can not enter too few letters. Ex: `answer = ['continue', 'test', 'testicle']`, user can not input `t`, `te` or `tes` because it will be ambiguous. User can however input `test`, which is not.