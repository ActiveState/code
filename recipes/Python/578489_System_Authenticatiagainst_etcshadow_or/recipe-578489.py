#!/usr/bin/env python

from os import path
from crypt import crypt
from re import compile as compile_regex


def check_auth(user, password):
    """Perform authentication against the local systme.

    This function will perform authentication against the local system's
    /etc/shadow or /etc/passwd database for a given user and password.

    :param user: The username to perform authentication with
    :type user: str

    :param password: The password (plain text) for the given user
    :type password: str

    :returns: True if successful, None otherwise.
    :rtype: True or None
    """

    salt_pattern = compile_regex(r"\$.*\$.*\$")
    passwd = "/etc/shadow" if path.exists("/etc/shadow") else "/etc/passwd"

    with open(passwd, "r") as f:
        rows = (line.strip().split(":") for line in f)
        records = [row for row in rows if row[0] == user]

    hash = records and records[0][1]
    salt = salt_pattern.match(hash).group()

    return crypt(password, salt) == hash
