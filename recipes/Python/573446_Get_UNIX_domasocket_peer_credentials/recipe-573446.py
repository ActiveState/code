import struct

def getpeerid(sock):
    """ Get peer credentials on a UNIX domain socket.

        Returns a nested tuple: (uid, (gids)) """

    LOCAL_PEERCRED = 0x001
    NGROUPS = 16

#struct xucred {
#        u_int   cr_version;             /* structure layout version */
#        uid_t   cr_uid;                 /* effective user id */
#        short   cr_ngroups;             /* number of groups */
#        gid_t   cr_groups[NGROUPS];     /* groups */
#        void    *_cr_unused1;           /* compatibility with old ucred */
#};

    xucred_fmt = '2ih16iP'
    res = tuple(struct.unpack(xucred_fmt, sock.getsockopt(0, LOCAL_PEERCRED, struct.calcsize(xucred_fmt))))
    
    # Check this is the above version of the structure
    if res[0] != 0:
        raise OSError

    return (res[1], res[3:3+res[2]])
