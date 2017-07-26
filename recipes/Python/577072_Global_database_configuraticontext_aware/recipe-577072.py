# -*- coding: utf-8 -*-
# file: helpers/database.py
"""
This module provides a possibility to process a configuration file 
and load database connection information from that configuration.
To load configuration and open the configured connections 
the following code can be executed::
 
    from helpers import database
    database.fileConfig(CONF_FILE_NAME)
    
Here CONF_FILE_NAME is the name of the configuration file. 
See fileConfig(fileName) for more details.
All registered connection pools are closed automatically on exiting the script 
(using 'atexit' events)

A public databaseConfig variable is an instance of a private _DatabaseConfig class, 
and holds the connection pools.

Possible examples of the usage are::

    from helpers import database
    # find the database.conf file and use it as a database configuration
    database.fileConfig('database.conf');

    database.get_connection_pool_names()    # get all defined pool names
    pool_name = 'videoflip'
    database.has_connection_pool(pool_name) # check if the pool with pool_name is defined
    
    videoflip_pool = database.get_connection_pool(pool_name) # get videoflip pool
    
    with videoflip_pool.context('testing cursor', ContextType.TRANSACTIONAL ) as cur:
        cur.execute('SELECT 1')
        r = cur.fetchone()
        print r
    
Decorator 'connectionPoolAware(pool_name, argument_name=None)' can be used to mark methods 
with the defined parameters, to pass the named connection pool to the method every time it is called.
But this approach seems to be not so interesting, as one always can get a needed pool 
directry with database.get_connection_pool('pool_name') 

See documentation for class 'PersistentConnectionPoolWithContext' that is returned by all the methods 
returning connection pool of this module. 
 
"""

import logging
from contextlib import contextmanager
import psycopg2
from psycopg2.pool import PersistentConnectionPool
from psycopg2.extras import DictCursor
import ConfigParser
import threading
import os.path
import atexit
import collections


__all__ = [ 'databaseConfig', 
           'fileConfig', 
           'DEFAULT_DATABASE_CONFIGURATION_FILE_NAME',
           'ContextType', 
           'PersistentConnectionPoolWithContext',
           'get_connection_pool',
           'has_connection_pool',
           'get_connection_pool_names',
           'InvalidMethodException',
           'InvalidDatabaseConfigurationException' ]

class Error(Exception):
    pass

class InvalidMethodException(Error):
    pass

class InvalidDatabaseConfigurationException(Error):
    pass


########################################################################################
#
#  Find file on the python path (http://code.activestate.com/recipes/52224/)
#  This code is actually to be located in a utility library, just moved it here
#  to make the module code independent
#
########################################################################################

def _find(path, matchFunc):
    apath = os.path.abspath(path)
    if matchFunc(apath):
        return apath
    for dirname in sys.path:
        candidate = os.path.join(dirname, path)
        if matchFunc(candidate):
            return candidate
    raise IOError("Can't find file %s" % path)


def find_file(path):
    """Find a file in the python system path
    
    """
    return _find(path,matchFunc=os.path.isfile)


def find_dir(path):
    """Find a directory in the pathon system path
    
    """
    return _find(path,matchFunc=os.path.isdir)

########################################################################################
#
#  EasySafeConfigParser class
#
########################################################################################

class EasySafeConfigParser(SafeConfigParser):
    'This implementation addes get_default method, that does not raise NoOptionError and returning default value in case the option does not exist'
    
    def get_default(self, section, option, default=None):
        try : 
            return SafeConfigParser.get(self, section, option )
        except NoOptionError :
            return default

########################################################################################


databaseConfig = None
_logger = logging.getLogger('helpers.database')
_database_config_lock = threading.RLock()

DEFAULT_DATABASE_CONFIGURATION_FILE_NAME='database.conf'


def fileConfig(file_name=DEFAULT_DATABASE_CONFIGURATION_FILE_NAME):
    """
    Configure database pools from the given configuration file. 
    Database configuration section names should start with prefix 'database_' 
    a name after that prefix is used as name for the registered connection pool.
    
    Configuration file should be named database.conf (default name) and located 
    in the current directory or if not found there in the PYTHON_PATH directories.
    This makes it possible to have one global configuration file, and then 
    add a local one for debugging purposes. Note, that config data is not being 
    merged and the file, first found is being used as a config file.
    
    Typical configuration file can look like that::
      
        [database_testdb1]
        dbname=testdb1 
        host=localhost
        port=5453
        user=test 
        password=test
        encoding=latin1
        statement_timeout=0
        
        [database_testdb2]
        dbname=testdb2 
        host=localhost
        port=5454
        user=test 
        password=test
    
    After the database access is configured, you can access database pools like::
    
        from myvideo.helpers import database
        database.fileConfig()
        testdb2_pool = database.get_connection_pool('testdb2')
    
    """
    # find configuration file
    file_name = find_file( file_name )
    # create configuration
    global databaseConfig #IGNORE:W0603
    databaseConfig = _DatabaseConfig(os.path.abspath(file_name))


def get_connection_pool(pool_name, config_file_name=DEFAULT_DATABASE_CONFIGURATION_FILE_NAME):
    """Returns a connection pool with a given name
    
    @param pool_name: a connection pool name to look up
    """

    if databaseConfig is None :
        fileConfig(config_file_name)
    return databaseConfig.get_connection_pool(pool_name)


def get_connection_pool_set(pool_name, config_file_name=DEFAULT_DATABASE_CONFIGURATION_FILE_NAME):
    """Returns a set of connection pools with a given name
    
    @param pool_name: a connection pool name to look up
    """

    if databaseConfig is None :
        fileConfig(config_file_name)
    return databaseConfig.get_connection_pool_set(pool_name)


def has_connection_pool(pool_name, config_file_name=DEFAULT_DATABASE_CONFIGURATION_FILE_NAME):
    """True if a connection pool with a given name is registered
    
    @param pool_name: a connection pool name to look up
    """
    if databaseConfig is None :
        fileConfig(config_file_name)
    return databaseConfig.has_connection_pool(pool_name)


def get_connection_pool_names(config_file_name=DEFAULT_DATABASE_CONFIGURATION_FILE_NAME):
    """Returns all registered connection pool names"""

    if databaseConfig is None :
        fileConfig(config_file_name)
    return databaseConfig.get_connection_pool_names()


class _DatabaseConfig(object):
    """Private class holding database configuration and registered connection pools"""
    
    __slots__ = ('logger', 'cp', 'fileName', '_pool_map', '_pool_config_section_map')
    
    # define an atexit function to be called at exit for the created pools
    def _atexit_close_pool(self, connection_pool):
        if connection_pool:
            if not connection_pool.closed:
                self.logger.debug('Closing all connections of the connection pool %s', connection_pool.pool_name)
                connection_pool.closeall()
    
    def __init__(self, fileName):
        # Initialize logging
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug('Creating DatabaseConfig from file %s', fileName )
        self.fileName = fileName
        # load configuration
        self.cp = EasySafeConfigParser()
        self.cp.read(fileName) 

        with _database_config_lock:
            self._pool_config_section_map = {}
            self._pool_map = {}
            # initialize database connection pools
            for section_name in self.cp.sections() :
                s = section_name.split('_', 1)
                if s[0] != 'database' : continue
                pool_name = s[1]
                if not pool_name : continue
                self._pool_config_section_map[pool_name] = section_name
                pool_tuple = tuple( self.database_config_section_to_connection_pool_set(section_name, pool_name) )
                self._pool_map[pool_name] = pool_tuple
                
            if not self._pool_map :
                self.logger.error('Could not find any database configuration sections in the given configuration file %s', fileName )

    def reload(self):
        """
        Read database configuration. 
        Read configuration file and check if some parameters had been changed there. 
        If changed -- recreate pool and close the old one
        Also should recheck if the database connection are alive
        """
        # TODO: implement refreshing of the configuration
        pass

    def database_config_section_to_connection_pool_set(self, section_name, pool_name):
        """Read the given section name from the private config parser and create a corresponding connection pool.
        
        This pool does not try to connect to the database immediately (with minconn=0)
        """
        if not pool_name:
            pool_name = section_name
        if not self.cp.has_section(section_name) :
            raise ConfigParser.NoSectionError(section_name)
        
        hosts = self.cp.get_default(section_name, 'host', 'localhost').split(',')
        port = int( self.cp.get_default(section_name, 'port', 5432) )
        dbname = self.cp.get_default(section_name, 'dbname', 'postgres')
        common_dsn = ' '.join( '{0[0]}={0[1]}'.format(item) for item in self.cp.items(section_name) if item[0].lower() not in ('host','dsn','encoding','statement_timeout') )
        host_dsn_list = [ ( host, 'host={0} {1}'.format(host.strip(), common_dsn) ) for host in hosts if host.strip() ]
        if not host_dsn_list :
            raise ConfigParser.NoOptionError('host', section_name)
 
        try :
            encoding=self.cp.get(section_name, 'encoding')
        except ConfigParser.NoOptionError :
            encoding=None
        try :
            statement_timeout=self.cp.get(section_name, 'statement_timeout')
            statement_timeout=int(statement_timeout)
        except ConfigParser.NoOptionError :
            statement_timeout=None
        except ValueError :
            statement_timeout=None
            self.logger.warning("Database configuration section {0} contains option 'statement_timeout' that should be numeric, but the specified value is '{1}', skipping this option.".format(section_name, statement_timeout) )

        for i, ( host, dsn ) in enumerate( host_dsn_list ):
            pool_name_i = '{0}_{1}'.format(pool_name, i) if len(host_dsn_list) > 1 else pool_name
            connection_pool = PersistentConnectionPoolWithContext(pool_name_i, 
                                                                  minconn=0, 
                                                                  maxconn=5, 
                                                                  host=host, 
                                                                  port=port, 
                                                                  dbname=dbname, 
                                                                  encoding=encoding, 
                                                                  statement_timeout=statement_timeout, 
                                                                  dsn=dsn)
            self.logger.debug('Created a connection pool to {0} database with dsn: {1}'.format(pool_name_i, dsn))
            atexit.register(self._atexit_close_pool, connection_pool)
            yield connection_pool

    def get_connection_pool(self, pool_name):
        """Returns a connection pool with a given name
        
        @param pool_name: a connection pool name to look up
        """
        with _database_config_lock :
            pool_set = self._pool_map[pool_name]
            if isinstance(pool_set, collections.Sequence ):
                if len(pool_set) != 1:
                    raise InvalidMethodException('Trying to get a connection pool from defined set of pools') 
                return pool_set[0]
            else:
                return pool_set

    def get_connection_pool_set(self, pool_name):
        """Returns a set of connection pools with a given name
        
        @param pool_name: a connection pool name to look up
        """
        with _database_config_lock :
            pool_set = self._pool_map[pool_name]
            if isinstance(pool_set, collections.Sequence ): 
                return pool_set
            else :
                return tuple( pool_set )

    def has_connection_pool(self, pool_name):
        """True if a connection pool with a given name is registered
        
        @param pool_name: a connection pool name to look up
        """
        with _database_config_lock :
            return pool_name in self._pool_map
        
    def get_connection_pool_names(self):
        """Returns all registered connection pool names"""
        with _database_config_lock :
            return self._pool_map.keys()


def connectionPoolAware(pool_name, argument_name=None):
    """This decorator redefines the value of the decorated function argument named <pool_name> 
    and sets it to the connection pool named pool_name defined in the DatabaseConfig class. 
    
    Note: this decorator seems to have no practical use, as it is much easier to fetch 
          a needed connection pool by name using database.get_connection_pool('pool_name')
          directly inside the method. 
    
    Typical way of decorating the method would be::
    
        @connectionPoolAware(pool_name='slave', argument_name='slavePool')
        def test_database_method(slavePool=None)
            with slavePool.context('testing connection pool aware method') as cur
                cur.execute('SELECT VERSION()')
        
        # and then call the defined method like that
        test_database_method()
    """
    def decorator(f):
        """Function wrapper, that returns a callable that wraps decorated function 'f' (passed as a parameter)"""
        def executor(*argv, **kwargs):
            """Actual wrapper, that adds some new parameters to the decorated function 'f'"""
            if databaseConfig :
                if databaseConfig.has_connection_pool(pool_name) :
                    # calculate the argument name to be assigned
                    n = argument_name if argument_name is not None else pool_name
                    p = databaseConfig.get_connection_pool( pool_name )
                    if p :
                        kwargs[ n ] = p
                    else :
                        _logger.error( 'Pool named %s is not initialized', pool_name )
                else :
                    _logger.error( 'Pool named %s is not defined!', pool_name )
            else :
                _logger.error( 'Database configuration should be initialized with fileConfig(fileName) call.')
            f(*argv, **kwargs) #IGNORE:W0142
        return executor
    return decorator


class ContextType(object):
    """Context type to be used by the PersistentConnectionPoolWithContext.context() method.
    
    The values define bits, for the control of the context, to be returned:
    
    SIMPLE -- does nothing
    
    TRANSACTIONAL -- will commit the results if no error happened and rollback in case of database error
    
    DICT_CURSOR -- returns DictCursor, that can be accessed using column names together with the column indexes. 
                   Cannot be used with NAMED_CURSOR.
    
    NAMED_CURSOR -- return a named cursor, that uses CURSOR internally and is good for fetching large data sets. 
                    Cannot be used with DICT_CURSOR.
    
    CLOSE_CONNECTION -- forces a close of the connection, before returning it to the pool, 
                        actually leading to throwing of that closed connection away. 
                        This can be used in case we always need some fresh connections from the pool.
     
    """
    __slots__ = ()

    SIMPLE = 0
    TRANSACTIONAL = 1
    DICT_CURSOR = 2
    NAMED_CURSOR = 4
    CLOSE_CONNECTION = 8


class PersistentConnectionPoolWithContext(PersistentConnectionPool):
    """This class extends psycopy2 PersistentConnectionPool class and adds context() method,
    that returns a database cursor aware context manager that automatically fetches a connection from the pool, 
    and, if needed, commits the changes on exiting from the context. In case some exception happens in the context, 
    the connection is rolled back and exception is thrown further.
    """
    
    def __init__(self, pool_name, minconn, maxconn, host, port, dbname, encoding, statement_timeout, *args, **kwargs):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.pool_name = pool_name
        self.address = ( host, port, )
        self.dbname = dbname
        self.encoding = encoding
        self.statement_timeout = statement_timeout
        PersistentConnectionPool.__init__(self, minconn, maxconn, *args, **kwargs) #IGNORE:W0142

    def _connect(self, key=None):
        conn = PersistentConnectionPool._connect(self, key)
        if self.encoding and conn.encoding and conn.encoding.lower() != self.encoding.lower() :
            conn.set_client_encoding(self.encoding)
        debug_string = 'Pool {0} created new connection with {1} encoding'.format( self.pool_name, conn.encoding )
        if self.statement_timeout is not None :
            cur = conn.cursor()
            try:
                # one can improve this by getting an old statement timeout value and then restoring it on 
                # reterning connection back to the pool 
                cur.execute('set STATEMENT_TIMEOUT to %s;', ( self.statement_timeout, ))
            except psycopg2.Error as e :
                self.logger.error('Could not set connection statement_timeout to {0}: {1}'.format( self.statement_timeout, e ) )
                conn.rollback()
            finally:
                cur.close()
                del cur
                conn.commit()
                debug_string += ' and statement_timeout set to {0} ms'.format(self.statement_timeout)
        self.logger.debug(debug_string + '.')
        del debug_string
        return conn

    @contextmanager
    def context(self, description, contextType=ContextType.DICT_CURSOR, cursorName=None):
        """Return a context of the cursor to be used with the pool. 
        The following example code can be used to demonstrate the way this context is to be used::
            
            with pool.context('experimenting with pool context', ContextType.TRANSACTIONAL | ContextType.CLOSE_CONNECTION ) as cur :
                cur.execute('SELECT 1')
                cur.fetchall()
                
            # as we are out of the context, cursor is closed, transaction is committed and 
            # connection is closed (as requested by the parameters)
        
        @param description: a description of the cursor that we are getting within this context, 
                            this string should answer the question 'what is the cursor needed for?'
        @param contextType: a bitmap defined by combining ContextType flags. Default is ContextType.DICT_CURSOR.
        @param cursorName:  a name for the named cursor. Should be defined when using ContextType.NAMED_CURSOR.
        """
        if ( contextType & ContextType.NAMED_CURSOR ) > 0 :
            if cursorName is None :
                cursorName = 'undefined'
        d = 'for ' + str(description) if description is not None else ''
        conn = self.getconn()
        
        if ( contextType & ContextType.DICT_CURSOR ) > 0 :
            cur = conn.cursor(cursor_factory=DictCursor)
            self.logger.debug("Got dict cursor %s", d)
        elif ( contextType & ContextType.NAMED_CURSOR ) > 0 :
            cur = conn.cursor(cursorName)
            self.logger.debug("Got named cursor(%s) %s", cursorName, d)
        else :
            cur = conn.cursor()
            self.logger.debug("Got generic cursor %s", d)
        try:
            yield cur
        except:
            if ( contextType & ContextType.TRANSACTIONAL ) > 0 :
                conn.rollback()
                self.logger.error("Rolling back transaction of cursor %s", d)
            raise
        else:
            if ( contextType & ContextType.TRANSACTIONAL ) > 0 :
                conn.commit()
                self.logger.debug("Committed transaction of cursor %s", d)
        finally:
            cur.close()
            if ( contextType & ContextType.CLOSE_CONNECTION ) > 0 :
                self.putconn(conn, close=True)
                self.logger.debug("Closed cursor %s and connection", d)
            else :
                self.putconn(conn)
                self.logger.debug("Closed cursor %s", d)


def _test():
    logging.getLogger().setLevel(logging.DEBUG)
    fileConfig()
    testdb1_pool = get_connection_pool('testdb1')
    testdb2_pool = get_connection_pool('testdb2')
    
    with videoflip_pool.context('getting test context to testdb1') as curs:
        curs.execute('SELECT %s::text as foo', ( 'Ã Ã¨Ã¬Ã²Ã¹', ) )
        r = curs.fetchone()
        print curs.statusmessage, r

    with master_pool.context('getting test context to testdb2') as curs:
        curs.execute('SELECT %s::text as foo', ( 'Ã Ã¨Ã¬Ã²Ã¹', ) )
        r = curs.fetchone()
        print curs.statusmessage, r

if __name__ == '__main__':
    _test()
