import ConfigParser
import string

_ConfigDefault = {
    "database.dbms":            "mysql",
    "database.name":            "",
    "database.user":            "root",
    "database.password":        "",
    "database.host":            "127.0.0.1"
    }

def LoadConfig(file, config={}):
    """
    returns a dictionary with key's of the form
    <section>.<option> and the values 
    """
    config = config.copy()
    cp = ConfigParser.ConfigParser()
    cp.read(file)
    for sec in cp.sections():
        name = string.lower(sec)
        for opt in cp.options(sec):
            config[name + "." + string.lower(opt)] = string.strip(cp.get(sec, opt))
    return config

if __name__=="__main__":
    print LoadConfig("some.ini", _ConfigDefault)
