## Funny text generator

Originally published: 2011-12-18 07:31:13
Last updated: 2011-12-25 11:14:39
Author: Pierre Quentel

This class takes a text (preferably long enough) and generates another text that "looks like" the original. It won't mean anything, or just by chance ;-)\n\nFor example, taking Hamlet, Act I, the program generates things like :\n\nHamlet\n\n>   And vanish'd from our watch;   \n>   His further. Fare third nights of the flushing immortal as it draw you into the flushing thy complete steel   \n>   'Tis sweet and each new-hatch'd:   \n>   A country's father;   \n>   To business and is prodigal thee!   \n>   Have of crowing more the should I have heaven,   \n>   Forward, therefore as ourself in the business it, Horatio   \n>   To what is't that your watch, bid this here!   \n\nUsage :\n\n    generator = TextGenerator(txt)\n    result = generator.random_text(3000)\n