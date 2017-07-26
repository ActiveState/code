import _mysql

table_prefixes = ["users","activities"]

def writedeps(db, tbl):
    db.query("show create table %s"%tbl)
    r = db.store_result()
    row = r.fetch_row()
    while row:
        for i in (x.strip() for x in row[0][1].split("\n")):
            if i.startswith("CONSTRAINT"):
                pieces = i.split()
                local = remote = None
                for idx, j in enumerate(pieces):
                    if j == "KEY":
                        local = pieces[idx+1].replace("`","").replace("(","").replace(")","")
                    if j == "REFERENCES":
                        remote = pieces[idx+1].replace("`","")
                print '"%s" -> "%s" [label="%s"];'%(tbl,remote,local)
        row = r.fetch_row()

def get_tables(db):
    db.query("show tables")
    r = db.store_result()
    row = r.fetch_row()
    while row:
        prefix = row[0][0].split("_")[0]
        if prefix in table_prefixes:
            yield row[0][0]
        row = r.fetch_row()    
    
def main():
    db=_mysql.connect("localhost","nibrahim","foo","sample")
    print "Digraph F {\n"
    print 'ranksep=1.5; size = "17.5,7.5";rankdir=LR;'
    for i in get_tables(db):
        writedeps(db, i)
    print "}"
        

if __name__ == "__main__":
    import sys
    sys.exit(main())
