from random import seed, shuffle
from string import ascii_lowercase as alphabet
from string import ascii_uppercase as capitals
from string import maketrans as mt
from sys import argv, exit

""" some cypherin' tricks
"""

long_message = """
anztheX yhnC -

"?ffbepn frzbp ru jbu bg qrfbccb fn ,gutve fv
 ag - rfhnc fergebcre xfn bg obw lz gv g'afV" ,friyrfzrug xfn gfnry gn gutvz lrug gnug - rfhnc fergebcre
 rivt qyhbj rparverckrheg ruGfrqabp rug ugvj tabyn frbt tavgebcre fjra uphz lnj rug fv ,uthbug ,tavug qnf lyheg ruGfrqabp rug ugvj tabyn frbt tavgebcre fjra uphz lnj rug fv ,uthbug ,tavug qnf lyheg ruG

.ugebj-syrf sb rfarf evrug ab xpnggn an f'gv
 - pvtby pvfno eb fgpns evrug ab ch ajbuf re'lrug aruj rtne ugvj gpnre rycbrc uphf ,arug ,lyongviraV

)".rxvy fqahbf abferc yhsguthbug n gnuj sb nrqv f'abferc qvchgf n rxvy f'rU" :fhug lrzeN xpvQ qrovepfrq
 rpab avryX nemR( .genzf qahbf zrug frxnz fvug gnug srvyro rug av zrug gnrcre qan ,frqhgvgnyc rfbug ch
 xpvc bg qarg fhbvehpav lyynhgpryyrgav ren gho fpvgvybc ghbon ftavyrrs tabegf rinu buj rycbrC .frqhgvgnyc
 rivgnierfabp sb rab lytavzyrujerib fv rfvba qahbetxpno rug ,rehgyhp ynpvgvybc gareehp ehb av :gv rrf V
 jbu f'rerU .uphz bf gba ,rZ .lgvehprfav ynhgpryyrgav f'gutve rug lo qrymmhc syrfzvu frffrsbec gvnuP

?gba luJ .ba ghO .lqnynz fvug sb rfehbpfvq ehb qrehp rinu qyhbj - sshgf
 tavjbax lyynhgpn ebs qrufvahc fnj rebT yN rfhnpro lyrfvprec rfhbU rgvuJ rug sb rpangfvq qnup-tavtanu
 avugvj gbt buj - ufhO .J rtebrT ugvj rparverckr f'abvgna rug gnug qrcbu ,gvzqn bg rinu V ,qnu V

.tavqarpfrqabp qan gantbeen fn ffbepn rznp ru ,rrf hbl - rtanupkr rug gfby rinu bg qrerqvfabp fv O abferC qaN

".fgpns rug ren reru - rgvuj g'afv xpnyo ,bA" ,flnf O abferC .rgnpfhsob bg gebssr rgnerovyrq n sb ghb argsb
rebz uthbugyn ,rpanebatv sb ghb fcnuerc - "rgvuj fv xpnyO" flnf N abferC :fvug rxvy frbt gV

.ghbon tavxyng re'lrug gnuj tavjbax lyynhgpn ebs qrufvahc ren frehtvs pvyohC


""".encode("rot13")[-1:0:-1] # somewhat obscured in case you actually want to solve it after you read the code

# print long_message # uncomment to cheat

def make_cypher(Seed=None):
    """ returns a shuffled alphabet 

    return is random if Seed not provided 
    return is repeatable function of Seed if provided
    """

    if Seed:
        seed(Seed)
    L = (list(alphabet))
    shuffle(L)
    return "".join(L)

def encrypt_factory(cypher = None,Seed = None):
    """ creates an encryptor and a decryptor function from a cypher, or a seed, or randomly
    """

    if not cypher:
        cypher = make_cypher(Seed)
    trans = mt(alphabet,cypher)
    untrans = mt(cypher,alphabet)
    def encryptor(message):
        return message.lower().translate(trans)
    def decryptor(message):
        return message.lower().translate(untrans)
    return encryptor, decryptor

def strip_cases(mixed_message):
    """ returns a lowercase version of input and a corrsponding list of booleans for case changes 

    note: ASCII
    """

    return mixed_message.lower(), [ch in capitals for ch in mixed_message]

def restore_cases(lower_message,cases):
    """ applies a list of case changes to a message; assumes input message all lowercase 

    note: ASCII
    """

    assert len(lower_message) == len(cases)
    return "".join([case and ch.upper() or ch for (ch,case) in zip(lower_message,cases)])

if __name__ == "__main__":

    """
    #tests

    message = "Python rocks"

    #stripping, restoring cases

    message_l,cases = strip_cases(message) 
    assert message == restore_cases(message_l,cases)

    # basic usage (random encryptor)

    encryptor,decryptor = encrypt_factory()
    assert decryptor(encryptor(message)) == message.lower()

    # prespecified encryptor
    rot13 = alphabet[13:] + alphabet[:13]
    e2,d2 = encrypt_factory(rot13) # rot13 repeated is a null operation
    assert e2(e2(message)) == message.lower()
    
    # repeatability, also demonstrates the relation between the two-step and one-step approach

    e3,d3 = encrypt_factory(Seed=1234)
    cypher = make_cypher(1234)
    e4,d4 = encrypt_factory(cypher) # these will be the same because the random seed is set
    assert d4(e3(message)) == message.lower() # so the decryption works

    # tests pass!
    """

    # play the game

    # You can provide text from a file; alter this ad lib
    # note: apply .encode("rot13")[-1:0:-1] to a string to obscure it; 
    # apply again to unobscure it

    if len(argv) > 1:
        long_message = file(argv[1]).read().encode("rot13")[-1:0:-1]

    # random encrypt/decrypt pair

    E,D = encrypt_factory(Seed = seed())

    # save uppercase info as a list of booleans

    long_l,cases2 = strip_cases(long_message)

    # encode

    cyphertext = E(long_message)

    # display coded message
        
    print "\n\n"+80*"="
    print restore_cases(cyphertext,cases2)
    print 80*"="
    
    # collect up the coded symbols in the message

    cypherbet = "".join([ch for ch in alphabet if ch in cyphertext])

    # wait for the user to provide an answer
    
    print "enter the decyphered alphabet below the letters of the code"

    # print D(" ".join(cypherbet)) # uncomment to cheat

    answer = None
    try:
        while not answer:
            answer = raw_input(" ".join(cypherbet)+"\n")
            if not answer:
                print "Please enter some text or ^C to exit"
            else:
                decypher = "".join([ch for ch in answer if ch.isalpha()])
                if len(decypher) != len(cypherbet):
                    print "\nPlease enter the correct number of characters."
                    answer = ""
    except KeyboardInterrupt:
        print "Thanks for trying!"
        exit()

    # test answer

    decypher_table = mt(cypherbet,decypher)

    print 80*"="

    try:
        assert cyphertext.translate(decypher_table) == long_message.lower()
    except:
        print "\n\nSorry. It should have been:\n%s\n%s" % (" ".join(cypherbet)," ".join(D(cypherbet)))
    else:
        print "\n\nYes!\n"
    
