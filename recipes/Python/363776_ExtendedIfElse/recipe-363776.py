def doLoginAction(self):
    """Try to actually log the user in."""
    class PasswordAccepted(Exception): pass
    try:
        if check_password():        # This may raise KeyError.
            raise PasswordAccepted
        do_more_expensive_work()
        and_even_more_expensive_work()
        if check_other_password():  #  This may raise KeyError.
            raise PasswordAccepted
        raise KeyError
    except KeyError:
        self.setError("Invalid username or password.")
        return
    except PasswordAccepted:
        pass
    continue_successfully()
