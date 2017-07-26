# Simple Infix Expression Evaluation Using A Stack
# The expression must be fully parenthesized
# (meaning 1+2+3 must be expressed as "((1+2)+3)")
# and must contain only positive numbers
# and aritmetic operators.
# FB - 20151107
def Infix(expr):
    expr = list(expr)
    stack = list()
    num = ""
    while len(expr) > 0:
        c = expr.pop(0)
        if c in "0123456789.":
            num += c
        else:
            if num != "":
                stack.append(num)
                num = ""
            if c in "+-*/":
                stack.append(c)
            elif c == ")":
                num2 = stack.pop()
                op = stack.pop()
                num1 = stack.pop()
                if op == "+":
                    stack.append(str(float(num1) + float(num2)))
                elif op == "-":
                    stack.append(str(float(num1) - float(num2)))
                elif op == "*":
                    stack.append(str(float(num1) * float(num2)))
                elif op == "/":
                    stack.append(str(float(num1) / float(num2)))
    return stack.pop()

expr = "((1.7+((2.8*3.6)/(0-9.4)))-5)"
print expr
print Infix(expr), eval(expr)
