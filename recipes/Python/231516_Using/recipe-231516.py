# start --- config.ini ---
# --*-- python --*--

enemy = "Dr. No"
salary = 100

def tax(salary):
   return salary * 0.2


bond = employee(id = "007", salary=salary * 2, tax=tax(salary * 2))

# end --- config.ini ---

# start --- readconf.py ---
class employee:
    def __init__(self, id, salary, tax):
        self.id = id
        self.salary = salary
        self.tax = tax

#FIXME: No error checking is done (to simplify code)
def read_conf(filename, optnames):
    '''Read configuration file return elements hash'''
    # Load file & eval
    h = {}
    execfile(filename, globals(), h)
    # Get only what we want 
    options = {}
    for item in h:
        if isinstance(h[item], employee) or (item in optnames):
            options[item] = h[item]

    return options

# end --- readconf.py ---
