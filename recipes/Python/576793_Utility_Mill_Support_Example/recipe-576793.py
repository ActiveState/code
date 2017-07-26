import expressions
import utility_mill
from test import support

################################################################################

def hard_test():
    while True:
        test = generate_test()
        with support.captured_stdout() as out:
            try:
                expressions.run(test, {})
            except Exception as err:
                print(err.args[0])
        val = out.getvalue()[:-1]
        try:
            out = utility_mill.run_latest('Expression_Evaluator', INPUT=test)
        except:
            pass
        else:
            print('PASS' if val == out else 'FAIL')

################################################################################

def soft_test():
    # test once a minute (softer)
    import time
    # we use some smart variables
    FAIL = 5
    NAME = 'Expression_Evaluator'
    # enter the main program code
    while True:
        version = get_version(FAIL, NAME)
        for minute in range(60):
            test = generate_test()
            with support.captured_stdout() as out:
                try:
                    expressions.run(test, {})
                except Exception as err:
                    print(err.args[0])
            val = out.getvalue()[:-1]
            out = get_results(FAIL, NAME, version, INPUT=test)
            print('PASS' if val == out else 'FAIL')
            time.sleep(60)

def get_version(fail, name):
    for attempt in range(fail):
        try:
            return utility_mill.get_version(name)
        except:
            pass
    raise SystemExit(1)

def get_results(fail, name, version, **query):
    for attempt in range(fail):
        try:
            return utility_mill.get_results(name, version, query)
        except:
            pass
    raise SystemExit(2)

################################################################################

import random
SR = random.SystemRandom()
LIB = '!"#$%&\'()*+,-./0123456789:<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
OP = '=', '+', '-', '*', '/', '//', '\\', '%', '**', '^', 'and', '&&', '&', 'or', '||', '|', '==', '!=', '>', '<', '>=', '=>', '<=', '=<'
MAX = 5

################################################################################

def generate_test():
    variables = set()
    required_lines = SR.randint(0, MAX)
    lines = []
    while len(lines) != required_lines:
        create_line(lines, variables)
    return '\n'.join(lines)

def create_line(lines, variables):
    required_expressions = SR.randint(0, MAX)
    expressions = []
    while len(expressions) != required_expressions:
        create_expression(expressions, variables)
    lines.append(';'.join(expressions))

def create_expression(expressions, variables):
    choice = SR.choice(['assign', 'comment', 'empty', 'print'])
    if choice == 'assign':
        tokens = create_assign(variables)
        variables.add('_')
    elif choice == 'comment':
        tokens = create_comment()
    elif choice == 'empty':
        tokens = []
    else:
        tokens = pad(create_evaluation(variables))
        variables.add('_')
    expressions.append(''.join(tokens))

def create_assign(variables):
    required_variables = SR.randint(1, MAX)
    new_variables = []
    while len(new_variables) != required_variables:
        create_variable(new_variables)
    tokens = []
    for variable in new_variables:
        tokens.append(variable)
        tokens.append('=')
    evaluation = create_evaluation(variables)
    variables.update(new_variables)
    tokens.extend(evaluation)
    padded_tokens = pad(tokens)
    return padded_tokens

def create_variable(new_variables):
    required_length = SR.randint(1, MAX)
    variable = ''
    while not valid_variable(variable):
        variable = []
        while len(variable) != required_length:
            variable.append(SR.choice(LIB))
        variable = ''.join(variable)
    new_variables.append(variable)

def valid_variable(variable):
    if not variable:
        return False
    if variable[0] == '#':
        return False
    try:
        float(variable)
        return False
    except:
        pass
    if variable in OP:
        return False
    return True

def create_evaluation(variables):
    required_tokens = SR.randint(1, MAX)
    tokens = []
    while len(tokens) != required_tokens:
        if SR.randint(0, 1):
            tokens.append(repr(SR.randint(1, 10)))
        elif variables:
            tokens.append(SR.choice(list(variables)))
    token_list = []
    for token in tokens:
        token_list.append(token)
        token_list.append(SR.choice(OP[1:]))
    return token_list[:-1]

def pad(tokens):
    token_list = []
    for token in tokens:
        token_list.append(token)
        token_list.append(create_whitespace())
    return token_list[:-1]

def create_whitespace():
    required_length = SR.randint(1, MAX)
    whitespace = []
    while len(whitespace) != required_length:
        if SR.randint(0, 1):
            whitespace.append(' ')
        else:
            whitespace.append('\t')
    return ''.join(whitespace)

def create_comment():
    required_length = SR.randint(1, MAX)
    tokens = ['#']
    while len(tokens) != required_length:
        create_variable(tokens)
    padded_tokens = pad(tokens)
    return padded_tokens

################################################################################
    
if __name__ == '__main__':
    soft_test()
