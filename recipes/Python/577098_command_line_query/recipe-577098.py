def command_line_query(question, default=None, validate=None, style="compact"):
    """Ask the user a question using raw_input() and looking something
    like this ("compact" style, the default, `_` is the cursor):

        QUESTION [DEFAULT]: _
        ...validation...

    or this ("verbose" style):

        QUESTION
        Hit <Enter> to use the default, DEFAULT.
        > _
        ...validation...

    @param question {str} The question to ask.
    @param default {str} Optional. The default value if non is given.
    @param validate {str|function} is either a string naming a stock
        validator

            not-empty       Ensure the user's answer is not empty.
            yes-or-no       Ensure the user's answer is 'yes' or 'no'.
                            ('y', 'n' and any capitalization are
                            also accepted)
            int             Answer is an integer.

        or a callback function with this signature:
            validate(answer) -> normalized-answer
        It should raise `ValueError` to indicate an invalid answer.
            
        By default no validation is done.
    @param style {str} is a name for the interaction style, either "compact"
        (the default) or "verbose". See the examples above.
    @returns {str} The normalized answer.
    """
    if isinstance(validate, (str, unicode)):
        if validate == "not-empty":
            def validate_not_empty(answer):
                if not answer:
                    raise ValueError("You must enter some non-empty value.")
                return answer
            validate = validate_notempty
        elif validate == "yes-or-no":
            def validate_yes_or_no(answer):
                normalized = {"yes":"yes", "y":"yes", "ye":"yes",
                    "no":"no", "n":"no"}
                try:
                    return normalized[answer.lower()]
                except KeyError:
                    raise ValueError("Please enter 'yes' or 'no'.")
            validate = validate_yes_or_no
        elif validate == "int":
            def validate_int(answer):
                try:
                    int(answer)
                except ValueError:
                    raise ValueError("Please enter an integer.")
                else:
                    return answer
            validate = validate_int
        else:
            raise ValueError("unknown stock validator: '%s'" % validate)
    
    def indented(text, indent=' '*4):
        lines = text.splitlines(1)
        return indent + indent.join(lines)

    if style == "compact":
        prompt = question
        if default is not None:
            prompt += " [%s]" % (default or "<empty>")
        prompt += ": "
    elif style == "verbose":
        sys.stdout.write(question + '\n')
        if default:
            sys.stdout.write("Hit <Enter> to use the default, %r.\n" % default)
        elif default is not None:
            default_str = default and repr(default) or '<empty>'
            sys.stdout.write("Hit <Enter> to leave blank.\n")
        prompt = "> "
    else:
        raise ValueError("unknown query style: %r" % style)
    
    while True:
        if True:
            answer = raw_input(prompt)
        else:
            sys.stdout.write(prompt)
            sys.stdout.flush()
            answer = sys.stdout.readline()
        if not answer and default:
            answer = default
        if validate is not None:
            orig_answer = answer
            try:
                norm_answer = validate(answer)
            except ValueError, ex:
                sys.stdout.write(str(ex) + '\n')
                continue
        else:
            norm_answer = answer
        break
    return norm_answer
