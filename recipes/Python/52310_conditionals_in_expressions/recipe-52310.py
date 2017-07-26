# with an if-else:
def foobar(whop):
    if whop>"pohrw": return "foox"
    else: return "barbar"

# the equivalent in expression-form:
foobar = lambda whop: ("foox", "barbar")[whop<="pohrw"]

# in general, we MUST ensure the 'conditional' turns
# into a 0 or 1 -- the 'not' operator is handy for that:
# not needed in the if-else case:
def plok(anything):
    if anything: return "xok"
    else: return "plik"

# but necessary when moving to expression-form:
plok = lambda anything: ("xok", "plik")[not anything]

# sometimes we need the shortcircuiting operators, 'and'
# and 'or', to avoid evaluating an incorrect expression:
def zod(plud):
    if plud: return 16+4/plud
    else: return 23

# must use and & or, NOT (...)[], as the operator-idiom:
zod = lambda plud: (plud and (16+4/plud)) or 23

# but if (16+4/plud)==0 [plud == -0.25] this erroneously
# returns 23!  A full solution ALSO requires indexing:
zod = lambda plud: ((plud and [16+4/plud]) or [23])[0]
# since the non-empty list [16+4/plud] is always 'true'
