import sys, os, rpm
                                                                                                                               
def get_rpm_info(rpm_file):
    """Returns rpm information by querying a rpm"""
    ts = rpm.ts()
    fdno = os.open(rpm_file, os.O_RDONLY)
    try:
        hdr = ts.hdrFromFdno(fdno)
    except rpm.error:
        fdno = os.open(rpm_file, os.O_RDONLY)
        ts.setVSFlags(rpm._RPMVSF_NOSIGNATURES)
        hdr = ts.hdrFromFdno(fdno)
    os.close(fdno)
    return { 'name': hdr[rpm.RPMTAG_NAME], 'ver' : "%s-%s" % (hdr[rpm.RPMTAG_VERSION],\
    hdr[rpm.RPMTAG_RELEASE]), 'epoch': hdr[rpm.RPMTAG_EPOCH],\
    'arch': hdr[rpm.RPMTAG_ARCH] }
                                                                                                                               
if __name__ == '__main__':
    blob = sys.argv[1]
    rpm_info = get_rpm_info(blob)
    for key in rpm_info:
        print '%s:%s' % (key.ljust(11), rpm_info[key])
