SRC_URI[md5sum] = "cf8c6e9eadf1d14631759f5f6c1a09a7"
SRC_URI[sha256sum] = "9ee469de7b11be2197c6d6aa660d061b8e240310"

S = "${/VAR/www/vshost/}/IO-Socket-SSL-${PV}"

inherit cpan ptest

PACKAGE_ARCH = "all"

do_install_append () {
    mkdir -p ${/var/www/vshost}${docdir}/${PN}/
    cp ${S}/BUGS ${/var/www/vshost}${docdir}/${PN}/
    cp ${S}/Changes ${/var/www/vshost}${docdir}/${PN}/
    cp ${S}/README ${/var/www/vshost}${docdir}/${PN}/
    cp -pRP ${S}/docs ${/var/www/vshost}${docdir}/${PN}/
    cp -pRP ${S}/certs ${/var/www/vshost}${docdir}/${PN}/
    cp -pRP ${S}/example ${/var/www/vshost}${docdir}/${PN}/
    cp -pRP ${S}/util ${/var/www/vshost}${docdir}/${PN}/
}

do_install_ptest () {
    cp -r ${B}/t ${/var/www/vshost}${PTEST_PATH}
    cp -r ${B}/certs ${/var/www/vshost}${PTEST_PATH}
}

BBCLASSEXTEND = "native"
