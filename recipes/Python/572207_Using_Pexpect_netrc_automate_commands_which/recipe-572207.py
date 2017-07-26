# ewp.py - John Landahl <john@landahl.org> [16 May 2008]

import sys, re, os, optparse, pexpect, netrc

def password_from_netrc(machine, user):
    '''Given a machine name and user name, return the associated password in
    ~/.netrc. Returns None if not found or if .netrc does not exist.'''
    password = None
    try:
        auth = netrc.netrc().authenticators(machine)
        if auth and auth[0] == user:
            password = auth[2]
    except IOError:
        pass
    return password

def execute_with_prompt(command, prompt, response, timeout=-1):
    '''Execute a system command which expects a single prompt (e.g. for a
    password) to be answered by the user before running.

    A timeout may be specified in seconds, where a value of -1 (a Pexpect
    convention) indicates that the default timeout (30 seconds) should be
    used.

    The result is a generator which produces each line of output as it is
    received from the command. This is especially advantageous for
    long-running commands or commands with a great deal of output, since the
    caller does not have to wait for the command to finish before receiving
    output, and the output will not take up memory as it would if collected
    into a list.

    Trailing CRLFs (included with each line coming from a pty) are stripped
    from each line.

    A simple example:

        for line in execute_with_prompt('sudo cat /etc/shadow', 'Password:', 'secret'):
            print line.split(':')[0:2]
    '''
    child = pexpect.spawn(command)
    child.expect(prompt, timeout=timeout)
    child.sendline(response)

    # compile a regular expression to find trailing CRLFs. note that we can't
    # simply use .rstrip() because it would strip -all- whitespace from the
    # end of each line, which could be inappropriate in some use cases.
    trailing_crlf = re.compile('\r\n$')

    # return a generator (via a generator expression) which will produce the
    # next line of output with each iteration.
    return (trailing_crlf.sub('', line) for line in child)

def main():
    '''
    Provide a generic wrapper around the password_from_netrc() and
    execute_with_prompt() functions, with some options for setting the
    machine, user, and prompt. The command to run should be the first argument
    and will most likely need to be put in quotes.

    Suppose our username is "foo" and we have a ~/.netrc file as follows:

      default login foo password secret
      default login bar password anothersecret
      machine blah login foo password y-a-secret

    If this script is saved as ewp.py, the default should allow for a simple
    command line:

      ewp.py "ssh somewhere ls /etc"

    This will provide ssh with the password 'secret' when prompted.

    If we need to login as as 'bar', the code here can determine this from the
    use of the @ symbol:

      ewp.py "ssh bar@somewhere ls /etc"

    This will provide ssh with the password 'anothersecret' when prompted.

    Finally, logging into the machine 'blah':

      ewp.py -m blah "ssh blah ls /etc"

    This will provide ssh with the password 'y-a-secret' when prompted. We had
    to use the '-m' flag here because the machine name cannot be determined
    automatically (there must be an @ symbol for the present code to work).
    '''
    opt = optparse.OptionParser()
    opt.add_option('--machine', '-m', dest='machine')
    opt.add_option('--user', '-u',    dest='user')
    opt.add_option('--prompt', '-p',  dest='prompt', default='ssword:')
    opts, args = opt.parse_args()

    command = args[0]
    machine = opts.machine
    user = opts.user

    # if machine or user were not specified, try to determine their values
    # from the command line
    if machine is None or user is None:
        match = re.search(r'(\w[\w\-.]+)@(\w[\w\-.]+)', command)
        if match:
            if user is None: user = match.group(1)
            if machine is None: machine = match.group(2)

        # fall-through case: use login name
        if user is None:
            user = os.getlogin()

    password = password_from_netrc(machine, user)

    # run an arbitrary command passed in as the first command line argument
    # (surround the full command with quotes).
    command = args[0]
    for line in execute_with_prompt(command, opts.prompt, password):
        print line

if __name__ == '__main__':
    main()
