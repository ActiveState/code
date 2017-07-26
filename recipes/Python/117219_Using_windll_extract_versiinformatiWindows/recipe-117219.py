# fileversion.py

import dynwin.windll as windll
import dynwin.oracle as oracle
import calldll
cstring = windll.cstring
version = windll.module('version')

vs_fixed_file_info = oracle.Oracle(
    'fixed file info structure',
    'Nllhhhhhhhhlllllll',
    ('signature',
     'struc_version',
     'file_version_msl',
     'file_version_msh',
     'file_version_lsl',
     'file_version_lsh',
     'product_version_msl',
     'product_version_msh',
     'product_version_lsl',
     'product_version_lsh',
     'file_flags_mask',
     'file_flags',
     'file_os',
     'file_type',
     'file_subtype',
     'file_date_ms',
     'file_date_ls')
    )

def _get_file_version_info_size(filename):
    return version.GetFileVersionInfoSize(cstring(filename), 0)

def _get_file_version_info(filename, verinfosize):
    buffer = windll.membuf(verinfosize)
    result = version.GetFileVersionInfo(cstring(filename),
                                        0,
                                        buffer.size(),
                                        buffer.address())
    return result, buffer

def _ver_query_value(buffer):
    verbufptr = windll.membuf(32)
    verbuflen = windll.membuf(32)
    result = version.VerQueryValue(buffer.address(),
                                   cstring('\\'),
                                   verbufptr,
                                   verbuflen)
    verbuffer = calldll.read_string(calldll.read_long(verbufptr),
                                    calldll.read_long(verbuflen))
    dict, size = vs_fixed_file_info.unpack(verbuffer)
    msh = str(dict['file_version_msh'])
    msl = str(dict['file_version_msl'])
    lsh = str(dict['file_version_lsh'])
    lsl = str(dict['file_version_lsl'])
    file_version = msh + '.' + msl + '.' + lsh + '.' + lsl
    return result, file_version

def get_file_version(filename):
    verinfosize = _get_file_version_info_size(filename)
    if not verinfosize: return None
    result, buffer = _get_file_version_info(filename, verinfosize)
    if not result: return None
    result, file_version = _ver_query_value(buffer)
    if not result: return None
    return file_version

if __name__ == '__main__':
    import os
    for file in os.listdir('c:\\winnt\\system32'):
        if not os.path.isdir(file):
            file_version = get_file_version(file)
            print file, file_version
