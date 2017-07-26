# -*- coding: iso-8859-1 -*-

#Copyright (C) 2004-2007 Dario Lopez-Kästen
#
#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA
#

"""
This module contains utility functions for
generating and checking passwords.

Default Password Properties Policy:
  - Minimum Password lenght is 8 tokens
  - At least four unique tokens
  - At least four character tokens
  - At least one number token
  - At least one special character token

NOTE: Crack check not implemented yet.

Provides access to Cracklib checking, IFF cracklib
is available as a python imported module. The
implementation of a Python Interface to Cracklib is left
as an excersise to the astute reader.

Adapted for future use of python-crack 0.5 by
#  Domenico Andreoli <cavok@filibusta.crema.unimi.it>
#  Web site at http://www.nongnu.org/python-crack/
# requires Cracklib 2.7
#  http://www.crypticide.com/users/alecm/

Only accepts/generates US-ASCII 7-bit tokens.
"""
import exceptions

##try:
##    import crack
from time import time

class PolicyNotEnforceable (exceptions.Exception):
    pass

# Our valid Token Set
vc  ='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
vn  = '0123456789'
vsc = ' !"#$%&''()*+,-./:;<=>?@[\]^_`{|}~'

# Our Password Policy Business Logic
min_unique_tokens    = 4
min_char_tokens      = 4
min_num_tokens       = 1
min_special_tokens   = 1
min_allowed_pwd_len  = 8

min_possible_pwd_len = min_char_tokens + min_num_tokens + min_special_tokens
min_unique_tokens_doable = (min_unique_tokens <= min_possible_pwd_len)

# Check at import time if the policy is enforceable

if min_allowed_pwd_len < min_possible_pwd_len:
    raise PolicyNotEnforceable, """
Minimal allowed password length (%s tokens) is too small in comparison
to the minimum possible password lenght (%s tokens).
"""%(str(min_allowed_pwd_len), str(min_possible_pwd_len))

if not min_unique_tokens_doable:
    raise PolicyNotEnforceable, """
Minimal amount of unique tokens (%s tokens) in password is larger than
the policys' minimum possible pwd lenght (%s tokens).
"""%(str(min_unique_tokens), str(min_possible_pwd_len))

def gen_passwd(pwd_len=min_allowed_pwd_len, strict_policy=0, seed=None):
    """
    Generates Paswords of pwd_len, that optinally strictly follows
    the Password Policy.

    if pwd_len < min_possible_len then policy cannot be enforced - if this happens,
    and strict_policy=1 it returns None.

    If pwd_len = min_possible_pwd_len then generate 4 unique tokens from vc, 1 token from
    vn and 1 token from vsc.

    if pwd_len > min_possible_pwd_len, then do as in previous step and then randomize the rest of the tokens.
    """

    # Basic and obvious input checking
    if strict_policy:
        if pwd_len < min_allowed_pwd_len:
            return None

    # Since we are generating passwords, we are nice to the poor
    # sods having to read and type them in, so we remove some
    # typcial character ambiguities. Yes, I know, this reduces the
    # Password Variation Space. See if I care - you're not the one
    # having to read the passwords or deal with complaints about that :-)
    # So, we reduce special chars
    rvs = vsc.replace(' ', '') # remove space
    rvs = rvs.replace('|', '') # remove pipe
    # reduce valid numbers
    rvn =  vn.replace('1', '') # remove nr 1
    rvn = rvn.replace('0', '') # remove zero
    # reduce valid chars
    rvc =  vc.replace('l', '') # remove lowercase L
    rvc = rvc.replace('I', '') # remove uppercase I
    rvc = rvc.replace('O', '') # remove uppercase O

    from random import Random
    if seed is None:
        seed = time() * time()
    gen = Random(seed)

    if not strict_policy:
        pl = gen.sample(rvc + rvn + rvs, pwd_len)
        return ''.join(pl)

    # We have a strict enforcement policy. Try for ten iterations, if not 
    # successfull then return None.
    rl_len = pwd_len - (min_char_tokens + min_num_tokens + min_special_tokens)
    for i in range(1,10):
        pl = gen.sample(rvc, min_char_tokens)    + \
             gen.sample(rvn, min_num_tokens)     + \
             gen.sample(rvs, min_special_tokens) + \
             gen.sample(rvc + rvn + rvs, rl_len)
        gen.shuffle(pl)
        pwd = ''.join(pl)
        err = check_passwd(pwd)
        if err == []:
            return pwd
    return None

def gen_num_passwd(pwd_len=min_allowed_pwd_len, seed=None):
    " Generates a numerical password only. No policy governs this password"
    from random import Random
    if seed is None:
        seed = time() * time()
    gen = Random(seed)
    pl = gen.sample(vn, pwd_len)
    return ''.join(pl)

def gen_char_passwd(pwd_len=min_allowed_pwd_len, seed=None):
    " Generates a password with characters only. No policy governs this password"
    from random import Random
    if seed is None:
        seed = time() * time()
    gen = Random(seed)
    pl = gen.sample(vc, pwd_len)
    return ''.join(pl)

def check_passwd(passwd):
    err = []
    pwd_len = len(passwd)
    # check length, if too short abort immediately
    # - no point in doing more checks
    if pwd_len < min_allowed_pwd_len:
        err.append('Password too short')
        return err

    # Check conditions, the naïve way
    utokens = [] # list of unique tokens, at least 4
    ctokens = [] # list of char tokens, at least 4
    ntokens = [] # list of number tokens, at least 1
    stokens = [] # list of special chars, at least 1
    nonval  = [] # list of non-valid tokens

    for c in passwd:
        isval = 0
        if c in vc:
            isval = 1
            ctokens.append(c)
        elif c in vn:
            isval = 1
            ntokens.append(c)
        elif c in vsc:
            isval = 1
            stokens.append(c)

        if not isval:
            nonval.append(c)
        elif c not in utokens:
            utokens.append(c)

    # Check for errors
    if len(nonval):
        err.append('Invalid %s tokens in passwd'%''.join(nonval))
    if len(utokens) < min_unique_tokens:
        err.append('Not at least %s unique tokens in passwd'%str(min_unique_tokens))
    if len(ctokens) < min_char_tokens:
        err.append('Not at least %s character tokens in passwd'%str(min_char_tokens))
    if len(ntokens) < min_num_tokens:
        err.append('Not at least %s number token in passwd'%str(min_num_tokens))
    if len(stokens) < min_special_tokens:
        err.append('Not at least %s special tokens in passwd'%str(min_special_tokens))

    if err:
        # We have errors - no point in doing more checks
        return err

    ## Check with cracklib
    #crk = crack()
    #try:
    #    crk.FascistCheck(passwd)
    #except ValueError, reason:
    #    err.append(reason)
    
    # Finally return err, whatever it is
    return err

def _create_generators(num, delta, firstseed=None):
    """Return list of num distinct generators.
    Each generator has its own unique segment of delta elements
    from Random.random()'s full period.
    Seed the first generator with optional arg firstseed (default
    is None, to seed from current time).
    """

    from random import Random
    g = Random(firstseed)
    result = [g]
    for i in range(num - 1):
        laststate = g.getstate()
        g = Random()
        g.setstate(laststate)
        g.jumpahead(delta)
        result.append(g)
    return result
