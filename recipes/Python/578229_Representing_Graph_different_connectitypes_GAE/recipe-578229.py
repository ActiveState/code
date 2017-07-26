from google.appengine.ext import db
from google.appengine.ext.db import polymodel
_connection_model_superclass = polymodel.PolyModel
class ConnectionModelMetaclass(type(_connection_model_superclass)):
    def __new__(cls, name, bases, dct):
        myname = name.replace('ConnectionModel','').lower()
        if myname:
            #this is not the baseclass
            to_collection_name = 'myto_%s_connections' % myname #or any other naming scheme you like
            from_collection_name = 'myfrom_%s_connections' % myname #or any other naming scheme you like
            myto = 'myto_%s'%myname
            myfrom = 'myfrom_%s'%myname
            dct[myto] = db.ReferenceProperty(collection_name = to_collection_name)
            dct[myfrom] = db.ReferenceProperty(collection_name = from_collection_name)
            if 'put' in dct:
                myput = dct['put']
            else:
                myput = None

            def put(self):
                setattr(self, myto, self.myto)
                setattr(self, myfrom, self.myfrom)
                self._validate_connected_types()
                if myput is not None:
                    myput(self)
                else:
                    MyClass = eval(name)
                    super(MyClass, self).put()
            dct['put'] = put
                
        return super(ConnectionModelMetaclass, cls).__new__(cls, name, bases, dct)
        
class ConnectionModel(_connection_model_superclass):
    __metaclass__ = ConnectionModelMetaclass
    ALLOWED_CONNECTIONS = {}#empty dict means anything goes. dict if of kind tuple->tuple
    timestamp = db.DateTimeProperty(auto_now = True)
    myto = db.ReferenceProperty(collection_name = 'myto_connections')
    myfrom = db.ReferenceProperty(collection_name = 'myfrom_connections')
    connection_index = db.StringProperty()#for strict sorting and paging of connections
    def _validate_connected_types(self):
        if None in (self.myfrom, self.myto):
            raise AttributeError
        if not self._check_connection():
            raise AttributeError(\
                'Connection %s --> %s is not allowed for class %s',
                self.myfrom.__class__.__name__,
                self.myto.__class__.__name__,
                self.__class__)
    
    def _check_connection(self):
        if len(self.ALLOWED_CONNECTIONS) == 0:
            return True
        for froms, tos in self.ALLOWED_CONNECTIONS.iteritems():
            if isinstance(self.myfrom, froms):
                if isinstance(self.myto, tos):
                    return True
        return False
        
    def put(self):
        if not self.connection_index:
            self.connection_index = '%s|%s|%s' % \
                    (self.timestamp, self.myfrom.key().name(),\
                        self.myto.key().name())
        super(ConnectionModel, self).put()

class LikeConnectionModel(ConnectionModel):
    ALLOWED_CONNECTIONS = {UserModel : ImageModel}
    
class FollowConnectionModel(ConnectionModel):
    ALLOWED_CONNECTIONS = {UserModel : (UserModel, ImageModel) }#users can follow users and (what the heck) follow images
     
