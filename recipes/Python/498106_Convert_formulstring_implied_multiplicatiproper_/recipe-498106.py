def toProperFormula(s):
    """
    Given formula string, returns a modified formula with missing 
    multiplication symbols and grouping symbols [],{} replaced by parentheses.

    Only primitive error checking for mismatched grouping symbols is shown in 
    this recipe.

    author: ernesto.adorio@gmail.com, ernie@extremecomputing.org
    """
    import tokenize
    from cStringIO import StringIO
    
    f          = StringIO(s)
    
    # Make variables mutable to child function.
    formula    = [""]
    prevtoken  = [""]
    prevsymbol = [""]
    closers    = []
    
    def handle_token(type, token, (srow, scol), (erow, ecol), line):
         token  = str(token)
         symbol = tokenize.tok_name[type]
         
         if symbol == "OP":
             if token == ")":
                if  closers.pop() != "(":  raise FormulaError('Error: "' +line[:ecol] + '" unbalanced ).')
             elif token == "]":
                if closers.pop() != "[":   raise FormulaError('Error: "' +line[:ecol] + '" unbalanced ].')
                token = ")"
             elif token == "}":
                if closers.pop() != "{":   raise FormulaError('Error: "' +line[:ecol] + '" unbalanced }.')
                token = ")"
             elif token in ["(", "[", "{"]:
                closers.append(token)
                if prevtoken[0] == ")" or prevsymbol[0] == "NUMBER":
                    formula[0] += "*"
                token = "("
         elif symbol in ["NAME", "NUMBER"]:
             if prevtoken[0] == ")" or prevsymbol[0] in ["NAME", "NUMBER"]:
                 formula[0] += "*"

         formula[0]    += token
         prevtoken[0]  =  token
         prevsymbol[0] =  symbol
        
    tokenize.tokenize(f.readline, handle_token)
    return formula[0]



print toProperFormula("2 ( 23.45x - 4y) [34 - 5 x] + w^[atan2(2y, 4x)] 5")

"""
2*(23.45*x-4*y)*(34-5*x)+w^(atan2(2*y,4*x))*5
"""
