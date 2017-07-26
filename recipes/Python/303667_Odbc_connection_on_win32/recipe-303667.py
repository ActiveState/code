from ctypes import *

#Costants
SQL_FETCH_NEXT = 1

SQL_INVALID_HANDLE		= -2
SQL_SUCCESS				= 0
SQL_SUCCESS_WITH_INFO	= 1
SQL_NO_DATA_FOUND		= 100

SQL_NULL_HANDLE = 0
SQL_HANDLE_ENV = 1
SQL_HANDLE_DBC = 2
SQL_HANDLE_DESCR = 4
SQL_HANDLE_STMT = 3

SQL_ATTR_ODBC_VERSION = 200
SQL_OV_ODBC2 = 2

SQL_TABLE_NAMES = 3

SQL_C_CHAR = 1

#Custom exceptions
class OdbcInvalidHandle(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
class OdbcGenericError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class FetchOdbcInfo:
    def __init__(self):
        self.odbc = windll.odbc32

    def connect_engine(self):
        #Connect to the engine. Return the enviroment and a connction handle
        env_h = c_int()
        dbc_h = c_int()
        stmt_h = c_int()
        
        self.odbc.SQLAllocHandle.restype = c_short
        ret = self.odbc.SQLAllocHandle(SQL_HANDLE_ENV, SQL_NULL_HANDLE, byref(env_h))
        if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
            self.ctrl_err(SQL_HANDLE_ENV, env_h, ret)

        self.odbc.SQLSetEnvAttr.restype = c_short
        ret = self.odbc.SQLSetEnvAttr(env_h, SQL_ATTR_ODBC_VERSION, SQL_OV_ODBC2, 0)
        if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
            self.ctrl_err(SQL_HANDLE_ENV, env_h, ret)

        self.odbc.SQLAllocHandle.restype = c_short
        ret = self.odbc.SQLAllocHandle(SQL_HANDLE_DBC, env_h, byref(dbc_h))
        if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
            self.ctrl_err(SQL_HANDLE_DBC, dbc_h, ret)

        return env_h, dbc_h
    
    def connect_odbc(self, dbc_h, dsn, user, passwd = ''):
        #Connect to odbc, return a statement handle
        stmt_h = c_int()
        sn = create_unicode_buffer(dsn)
        un = create_unicode_buffer(user)        
        pw = create_unicode_buffer(passwd)
        self.odbc.SQLConnect.restype = c_short
        ret = self.odbc.SQLConnect(dbc_h, sn, len(sn), un, len(un), pw, len(pw))
        if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
            self.ctrl_err(SQL_HANDLE_DBC, dbc_h, ret)

        self.odbc.SQLAllocHandle.restype = c_short
        ret = self.odbc.SQLAllocHandle(SQL_HANDLE_STMT, dbc_h, byref(stmt_h))
        if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
            self.ctrl_err(SQL_HANDLE_STMT, stmt_h, ret)

        return stmt_h

    def get_cols(self, stmt_h):
        #Return a list with all tables
        self.odbc.SQLTables.restype = c_short
        #We want only tables
        t_type = create_unicode_buffer('TABLE')
        ret = self.odbc.SQLTables(stmt_h, None, 0, None, 0, None, 0, byref(t_type), len(t_type))
        if not ret == SQL_SUCCESS:
            self.ctrl_err(SQL_HANDLE_STMT, self.stmt_h, ret)

        TableName = create_unicode_buffer(1024)
        buff_ind = c_int()
        self.odbc.SQLBindCol.restype = c_short
        ret = self.odbc.SQLBindCol(stmt_h, SQL_TABLE_NAMES, SQL_C_CHAR, byref(TableName), \
          len(TableName), byref(buff_ind))
        if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
            self.ctrl_err(SQL_HANDLE_STMT, self.stmt_h, ret)
            
        self.odbc.SQLFetch.restype = c_short
        table_list = []
        while 1:
            ret = self.odbc.SQLFetch(stmt_h)
            if ret == SQL_NO_DATA_FOUND:
                break
            elif not ret == SQL_SUCCESS:
                self.ctrl_err(SQL_HANDLE_STMT, stmt_h, ret)
            table_list.append(TableName.value)
        return table_list

    def enum_dsn(self, env_h):
        #Return a list with [name, descrition]
        dsn = create_unicode_buffer(1024)
        desc = create_unicode_buffer(1024)
        dsn_len = c_int()
        desc_len = c_int()
        dsn_list = []
        self.odbc.SQLDataSources.restype = c_short
        while 1:
            ret = self.odbc.SQLDataSources(env_h, SQL_FETCH_NEXT, \
                dsn, len(dsn), byref(dsn_len), desc, len(desc), byref(desc_len))
            if ret == SQL_NO_DATA_FOUND:
                break
            elif not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
                self.ctrl_err(SQL_HANDLE_STMT, stmt_h, ret)
            else:
                dsn_list.append((dsn.value, desc.value))
        return dsn_list

    def ctrl_err(self, ht, h, val_ret):
        #Method for make a control of the errors
        #Return a raise with a list
        state = create_unicode_buffer(5)
        NativeError = c_int()
        Message = create_unicode_buffer(1024*10)
        Buffer_len = c_int()
        err_list = []
        number_errors = 1
        self.odbc.SQLGetDiagRec.restype = c_short
        while 1:
            ret = self.odbc.SQLGetDiagRec(ht, h, number_errors, state, \
                NativeError, Message, len(Message), byref(Buffer_len))
            if ret == SQL_NO_DATA_FOUND:
                #No more data, I can raise
                raise OdbcGenericError, err_list
                break
            elif ret == SQL_INVALID_HANDLE:
                #The handle passed is an invalid handle
                raise OdbcInvalidHandle, 'SQL_INVALID_HANDLE'
            elif ret == SQL_SUCCESS:
                err_list.append((state.value, Message.value, NativeError.value))
                number_errors += 1
