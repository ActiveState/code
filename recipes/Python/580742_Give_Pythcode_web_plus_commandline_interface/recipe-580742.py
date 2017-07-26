"""
hug_pdp.py
Use hug with psutil to show disk partition info 
via Python, CLI or Web interfaces.
Copyright 2017 Vasudev Ram
Web site: https://vasudevram.github.io
Blog: http://jugad2.blogspot.com
Product store: https://gumroad.com/vasudevram
"""

import sys
import psutil
import hug

def get_disk_partition_data():
    dps = psutil.disk_partitions()
    fmt_str = "{:<8} {:<7} {:<7}"

    result = {}
    result['header'] = fmt_str.format("Drive", "Type", "Opts")
    result['detail'] = {}
    for i in (0, 2):
        dp = dps[i]
        result['detail'][str(i)] = fmt_str.format(dp.device, dp.fstype, dp.opts)
    return result

@hug.cli()
@hug.get(examples='drives=0,1')
@hug.local()
def pdp():
    """Get disk partition data"""
    result = get_disk_partition_data()
    return result

@hug.cli()
@hug.get(examples='')
@hug.local()
def pyver():
    """Get Python version"""
    pyver = sys.version[:6]
    return pyver

if __name__ == '__main__':
    pdp.interface.cli()
