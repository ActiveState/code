# Version 1.0   Ernie P. Adorio
#  
# 1. Data source rows as tuples, fields should form a hierarchy.
#    but the rows do not have to be in sorted order.
#            (Region, city, value)

records = [  ('England', 'Manchester', 45600),
             ('Scotland', 'Edinburgh', 20000),
             ('England', 'London', 90000),
             ('Scotland', 'Glasgow', 12500),
             ('Wales', 'Cardiff', 29700),
             ('England', 'Liverpool', 29700),
             ('Scotland', 'Edinburgh', 1000),
             ('Wales', 'Bangor', 12800),
             ('Scotland', 'Glasgow', 13400),
             ('England', 'Liverpool', 30000)]


# 2. Hierarchy levels and index of value to summarize.
maxlevel   = 2  # Maximum hierarchy levels  Region/city.
valueIndex = 2  # Index of value to summarize in data tuple.

# 3. Summaries in dictionary format.
Dlevels  = {}   
for rec in records:
    v = rec[valueIndex]
    for i in range(maxlevel):   # handle the sublevels 
        key = rec[:i+1]       
        if key not in Dlevels:
            Dlevels[key] = v
        else:
            Dlevels[key] += v

# 4. Schwartzian transform 
Tlevels = []
for  key in Dlevels:
    value = Dlevels[key]
    Tlevels.append((key, value))
Tlevels.sort()

# 5. Reporting (must be tailored to your actual requirements).
Total = 0
for (key, value) in enumerate(Tlevels):
    location = value[0]
    amt      = value[1]
    L        = len(location)

    if L == 1:  # Major category.
        Region  = location[0]
        print Region, "   \t", amt
        Total += amt
    else: 
        print " " * L,
        city    = location[1]
        print city, "\t\t",  amt
        
print "=" * 10
print "Total   \t", Total  
    

"""
When the program is run, it outputs
England         195300
   Liverpool            59700
   London               90000
   Manchester           45600
Scotland        46900
   Edinburgh            21000
   Glasgow              25900
Wales           42500
   Bangor               12800
   Cardiff              29700
==========
Total           284700
"""
    
        
    
