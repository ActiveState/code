import ctypes

ODBC_ADD_DSN = 1        # Add data source
ODBC_CONFIG_DSN = 2     # Configure (edit) data source
ODBC_REMOVE_DSN = 3     # Remove data source
ODBC_ADD_SYS_DSN = 4    # add a system DSN
ODBC_CONFIG_SYS_DSN = 5 # Configure a system DSN
ODBC_REMOVE_SYS_DSN = 6 # remove a system DSN

def create_sys_dsn(driver, **kw):
    """Create a  system DSN
    Parameters:
        driver - ODBC driver name
        kw - Driver attributes
    Returns:
        0 - DSN not created
        1 - DSN created
    """
    nul = chr(0)
    attributes = []
    for attr in kw.keys():
        attributes.append("%s=%s" % (attr, kw[attr]))
    
    return ctypes.windll.ODBCCP32.SQLConfigDataSource(0, ODBC_ADD_SYS_DSN, driver, nul.join(attributes))

if __name__ == "__main__":
    if create_sys_dsn("SQL Server",SERVER="(local)", DESCRIPTION="Northwind SQL Server DSN", DSN="NorthwindDSN", Database="Northwind", Trusted_Connection="Yes"):
        print "DSN created"
    else:
        print "DSN not created"
