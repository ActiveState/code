#!/usr/bin/env python26

# Nagios_sql.py - Matt Keranen 2011 (mksql@yahoo.com)

# FreeTDS: ./configure --with-tdsver=8.0 --enable-msdblib
# /etc/odbcinst.ini:
# [FreeTDS]
# Description = TDS driver for MSSQL
# Driver = /usr/local/lib/libtdsodbc.so

import getopt, platform, pyodbc, string, sys

nagios_codes = dict(OK=0, WARNING=1, CRITICAL=2, UNKNOWN=3, DEPENDENT=4)

def usage():
    nagios_return('UNKNOWN', 'usage: %s -h host -t test\n%s'% (format(sys.argv[0]), test_list()))

def nagios_return(code, response):
    print(code + ": " + response)
    sys.exit(nagios_codes[code])

def execute_sql(host, sql, database='master'):
    """Execute SQL against specified database"""
    if platform.system() == 'Darwin': driver = 'SQL Server'
    else: driver = 'FreeTDS'

    cs = r'DRIVER={%s};SERVER=%s;DATABASE=%s;UID=nagios;PWD=N^gm3;'  % (driver,host,database)

    try: cnx = pyodbc.connect(cs)
    except pyodbc.Error as e: return {'code':'CRITICAL', 'msg': "Unable to connect to SQL host %s\n%s" % (host, string.join(e,'\n'))}

    cur = cnx.cursor()
    try: rows = cur.execute(sql).fetchall()
    except pyodbc.Error as e:
        cnx.close()
        return {'code':"CRITICAL", 'msg': "Unable to execute SQL query on host %s\n%s" % (host, string.join(e,'\n'))}

    cur.close()
    cnx.close()

    return rows

def get_func(test):
    """Determine if function name is valid and defined as a Nagios test"""

    try: func = getattr(sys.modules[__name__], test)
    except AttributeError as e:
        nagios_return ('UNKNOWN', 'Invalid test name %s' % test)

    try: test = func.is_test
    except: nagios_return ('UNKNOWN', '%s not defined as test' % test)

    if test: return func
    else: nagios_return  ('UNKNOWN', '%s not defined as test' % test)

def test_list():
    """List of valid test names"""
    tests = 'tests:\n'
    for func in dir(sys.modules[__name__]):
        test = getattr(sys.modules[__name__], func)
        try: test.is_test
        except: pass
        else: tests += '  %s\n' % func

    return tests

def nagios_test(func):
    func.is_test = True
    return func


@nagios_test
def sql_ping(host):
    """Connect to SQL Server instance and return version string"""

    sql = 'SELECT @@VERSION'
    rows = execute_sql(host, sql)
    if type(rows) is dict: return rows

    message = rows[0][0]

    return {'code':'OK', 'msg': message}

@nagios_test
def db_state(host):
    """Check state of each database"""
    crit = warn = 0
    msg = ''

    sql = 'SELECT [name] db, user_access, user_access_desc, state, state_desc FROM sys.databases WHERE user_access > 0 OR state > 0'
    rows = execute_sql(host, sql)
    if type(rows) is dict: return rows

    for row in rows:
        if row.state == 6:
            warn += 1
            msg += 'Database %s is %s\n' % (row.db, row.state_desc)
        elif row.state > 3:
            crit += 1
            msg += 'Database %s is %s\n' % (row.db, row.state_desc)

        if row.user_access > 0:
            #warn += 1
            msg += 'Database %s in mode %s\n' % (row.db, row.user_access_desc)

    if crit > 0:
        code = 'CRITICAL'
        msg = 'Database state CRITICAL\n' + msg
    elif warn > 0:
        code = 'WARNING'
        msg = 'Database state warning\n' + msg
    else:
        code = 'OK'
        msg = 'Databases OK\n' + msg

    return {'code':code, 'msg': msg}

@nagios_test
def replication_status(host):
    """Report transactional replication status"""
    mstat = mwarn = 0
    msg = ''

    status = {0:'Unknown', 1:'Started', 2:'Succeeded', 3:'Active', 4:'Idle', 5:'Retrying', 6:'Failed'}
    warning = {0: '', 1:'-Expiration ', 2:'-Latency '}

    sql = 'EXEC dbo.sp_replmonitorhelppublication @publisher = @@SERVERNAME'
    rows = execute_sql(host, sql, 'distribution')
    if type(rows) is dict: return rows

    for row in rows:
        if row.status > mstat: mstat = row.status
        if row.warning > mwarn: mwarn = row.warning
        if row.worst_latency is None: row.worst_latency = 0
        msg += 'Pub:%s DB:%s Status:%s%s MaxLatency:%ss\n' % (row.publication, row.publisher_db, status[row.status], warning[row.warning], row.worst_latency)

    sql = 'EXEC dbo.sp_replmonitorhelpsubscription @publisher = @@SERVERNAME, @publication_type = 0'  # Transactional replication
    rows = execute_sql(host, sql, 'distribution')
    if type(rows) is dict: return rows

    for row in rows:
        if row.status > mstat: mstat = row.status
        if row.warning > mwarn: mwarn = row.warning
        if row.latency is None: row.latency = '?'
        msg += 'Sub:%s DB:%s Status:%s%s Latency:%ss\n' % (row.subscriber, row.subscriber_db, status[row.status], warning[row.warning], row.latency)

    if mstat == 6:
        code = 'CRITICAL'
        msg = 'Replication CRITICAL\n' + msg
    elif mstat == 5 or mwarn > 0:
        code = 'WARNING'
        msg = 'Replication WARNING\n' + msg
    else:
        code = 'OK'
        msg = 'Replication OK\n' + msg

    return {'code':code, 'msg': msg}

@nagios_test
def mirror_status(host):
    """Report mirror status"""
    crit = warn = 0
    msg = ''

    sql = """SELECT d.name dbname, m.mirroring_partner_instance partner, m.mirroring_state, m.mirroring_state_desc state
        FROM sys.databases d
        INNER JOIN sys.database_mirroring m ON m.database_id = d.database_id
        WHERE m.mirroring_state IS NOT NULL"""
    rows = execute_sql(host, sql)
    if type(rows) is dict: return rows

    #state = {0:'Suspended', 1:'Disconnected', 2:'Synchronizing', 3:'PendingFailover', 4:'Synchronized'}
    #sql = "EXEC sp_dbmmonitorresults '%s'" % dbname

    for row in rows:
        if row.mirroring_state < 2: crit += 1
        if row.mirroring_state == 3: warn += 1
        msg += "DB:%s Partner:%s State:%s\n" % (row.dbname, row.partner, row.state)

    if crit > 0:
        code = 'CRITICAL'
        msg = 'Mirroring CRITICAL\n' + msg
    elif warn > 0:
        code = 'WARNING'
        msg = 'Mirroring warning\n' + msg
    else:
        code = 'OK'
        msg = 'Mirroring OK\n' + msg

    return {'code':code, 'msg': msg}

@nagios_test
def logship_status(host):
    """Report log shipping retstore delta and latency"""
    crit = warn = 0
    msg = ''

    sql = """SELECT secondary_server, secondary_database, primary_server, primary_database,
        last_restored_date, DATEDIFF(mi, last_restored_date, GETDATE()) last_restored_delta,
        last_restored_latency, restore_threshold
        FROM msdb..log_shipping_monitor_secondary"""
    rows = execute_sql(host, sql)
    if type(rows) is dict: return rows

    for row in rows:
        if row.last_restored_delta >= row.restore_threshold:
            warn += 1
            msg += "Srv:%s DB:%s Restore delta %s exceeds threshold of %s\n" % (row.primary_server, row.primary_database, row.last_restored_delta, row.restore_threshold)
        if row.last_restored_latency >= row.restore_threshold:
            crit += 1
            msg += "Srv:%s DB:%s Latency of %s exceeds threshold of %s\n" % (row.primary_server, row.primary_database, row.last_restored_latency, row.restore_threshold)
        if row.last_restored_delta < row.restore_threshold and row.last_restored_latency < row.restore_threshold:
            msg += "Srv:%s DB:%s Latency:%s Restore delta:%s\n" % (row.primary_server, row.primary_database, row.last_restored_latency, row.last_restored_delta)


    if crit > 0:
        code = 'CRITICAL'
        msg = 'Log shipping CRITICAL\n' + msg
    elif warn > 0:
        code = 'WARNING'
        msg = 'Log shipping warning\n' + msg
    else:
        code = 'OK'
        msg = 'Log shipping OK\n' + msg

    return {'code':code, 'msg': msg}


def main():
    if len(sys.argv) < 2: usage()

    try: opts, args = getopt.getopt(sys.argv[1:], 'h:t:')
    except getopt.GetoptError as err: usage()

    host = test = None

    for o, value in opts:
        if o == "-h": host = value
        elif o == "-t": test = value
        else: usage()
    if host is None or test is None: usage()

    func = get_func(test)
    result = func(host)
    nagios_return(result['code'], result['msg'])

if __name__ == "__main__":
    main()
