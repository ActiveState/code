def query_custom_answers(question, answers, default=None):
    """Ask a question via raw_input() and return the chosen answer.
    
    @param question {str} Printed on stdout before querying the user.
    @param answers {list} A list of acceptable string answers. Particular
        answers can include '&' before one of its letters to allow a
        single letter to indicate that answer. E.g., ["&yes", "&no",
        "&quit"]. All answer strings should be lowercase.
    @param default {str, optional} A default answer. If no default is
        given, then the user must provide an answer. With a default,
        just hitting <Enter> is sufficient to choose. 
    """
    prompt_bits = []
    answer_from_valid_choice = {
        # <valid-choice>: <answer-without-&>
    }
    clean_answers = []
    for answer in answers:
        if '&' in answer and not answer.index('&') == len(answer)-1:
            head, sep, tail = answer.partition('&')
            prompt_bits.append(head.lower()+tail.lower().capitalize())
            clean_answer = head+tail
            shortcut = tail[0].lower()
        else:
            prompt_bits.append(answer.lower())
            clean_answer = answer
            shortcut = None
        if default is not None and clean_answer.lower() == default.lower():
            prompt_bits[-1] += " (default)"
        answer_from_valid_choice[clean_answer.lower()] = clean_answer
        if shortcut:
            answer_from_valid_choice[shortcut] = clean_answer
        clean_answers.append(clean_answer.lower())

    # This is what it will look like:
    #   Frob nots the zids? [Yes (default), No, quit] _
    # Possible alternatives:
    #   Frob nots the zids -- Yes, No, quit? [y] _
    #   Frob nots the zids? [*Yes*, No, quit] _
    #   Frob nots the zids? [_Yes_, No, quit] _
    #   Frob nots the zids -- (y)es, (n)o, quit? [y] _
    prompt = " [%s] " % ", ".join(prompt_bits)
    leader = question + prompt
    if len(leader) + max(len(c) for c in answer_from_valid_choice.keys() + ['']) > 78:
        leader = question + '\n' + prompt.lstrip()
    leader = leader.lstrip()

    valid_choices = answer_from_valid_choice.keys()
    if clean_answers:
        admonishment = "*** Please respond with '%s' or '%s'. ***" \
                       % ("', '".join(clean_answers[:-1]), clean_answers[-1])

    while 1:
        sys.stdout.write(leader)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return default
        elif choice in answer_from_valid_choice:
            return answer_from_valid_choice[choice]
        else:
            sys.stdout.write("\n"+admonishment+"\n\n\n")
