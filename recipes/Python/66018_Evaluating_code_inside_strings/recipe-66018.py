class Eval:
    def __getitem__(self, key):
        return eval(key)

number = 19
text = "python"

print "%(text.capitalize())s %(number/9.0).1f rules!" % Eval()

#Python 2.1 rules!
