def get_version_from_win32_pe(file):
    # http://windowssdk.msdn.microsoft.com/en-us/library/ms646997.aspx
    sig = struct.pack("32s", u"VS_VERSION_INFO".encode("utf-16-le"))
    # This pulls the whole file into memory, so not very feasible for
    # large binaries.
    try:
        filedata = open(file).read()
    except IOError:
        return "Unknown"
    offset = filedata.find(sig)
    if offset == -1:
        return "Unknown"

    filedata = filedata[offset + 32 : offset + 32 + (13*4)]
    version_struct = struct.unpack("13I", filedata)
    ver_ms, ver_ls = version_struct[4], version_struct[5]
    return "%d.%d.%d.%d" % (ver_ls & 0x0000ffff, (ver_ms & 0xffff0000) >> 16,
                            ver_ms & 0x0000ffff, (ver_ls & 0xffff0000) >> 16)
