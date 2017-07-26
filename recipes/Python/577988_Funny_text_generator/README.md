## Funny text generator  
Originally published: 2011-12-18 07:31:13  
Last updated: 2011-12-25 11:14:39  
Author: Pierre Quentel  
  
This class takes a text (preferably long enough) and generates another text that "looks like" the original. It won't mean anything, or just by chance ;-)

For example, taking Hamlet, Act I, the program generates things like :

Hamlet

>   And vanish'd from our watch;   
>   His further. Fare third nights of the flushing immortal as it draw you into the flushing thy complete steel   
>   'Tis sweet and each new-hatch'd:   
>   A country's father;   
>   To business and is prodigal thee!   
>   Have of crowing more the should I have heaven,   
>   Forward, therefore as ourself in the business it, Horatio   
>   To what is't that your watch, bid this here!   

Usage :

    generator = TextGenerator(txt)
    result = generator.random_text(3000)
