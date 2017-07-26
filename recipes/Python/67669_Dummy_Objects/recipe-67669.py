import sys
class Dummy:
    def __init__(self,identity = 'unknown'):
        self.identity = identity
        self.name = ''

    def call(self,*args):
        method = self.name + "("
        count = 1

        for o in args:
            if count != 1:
                method = method + ","
            method = method + repr(type(o))
            count = count + 1
            
        method = method + ")"
        try:
            raise "Dummy"
        except:
            line = 'Line ' +repr(sys.exc_info()[2].tb_frame.f_back.f_lineno)+': '
        raise AttributeError(line + method+" called on dummy "+self.identity+" Object\n")
        
    def __getattr__(self, name):
        self.name = name
        return self.call

if __name__ == '__main__':
    try:
        rect = ''
        rect = Dummy('Rectangle')#try also after commenting this line
        rect.GetWidth()
        rect.SetHeight(50)
        rect.SetColor('Red')
    except AttributeError,e:
        print e
