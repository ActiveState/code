"""
RecipePacker: 

Packs all python source files from current directory  into a single recipe file 
that can be later run to recreate packed files. 

Usage:  
Copy RecipePacker module into source directory.
Run RecipePacker module.
    - Creates _recipe directory and writes _recipe.py to _recipe directory.
Run _recipe.py.
    - Recreates packed files into containing directory.

Notes:
* Skips files whose names begin with underscore or contain "recipe".
* Hasn't been checked with unicode.
"""
__author__=["Jack Trainor (jacktrainor@gmail.com)",]
__version__="2010-07-20"

import os
import os.path
import re
    
class RecipePacker(object):
    SQUOTE_ESCAPE = "%SQ%"
    DQUOTE_ESCAPE = "%DQ%"
    SLASH_ESCAPE = "%SLASH%"
    TRIPLE_SQUOTE_ESCAPE = "%SQSQSQ%"
    TRIPLE_DQUOTE_ESCAPE = "%DQDQDQ%"
    RECIPE_DIR = "_recipe"
    RECIPE_PY = "_recipe.py"
    PROLOG = """import os
import os.path
import re

" RecipeUnpacker recreates a group of Python modules into current directory. "
" See http://code.activestate.com/recipes/577297-consolidate-group-of-modules-into-one-recipe/?in=lang-python "
__author__=["Jack Trainor (jacktrainor@gmail.com)",]
__version__="2010-07-20"
"""
    EPILOG = """
class RecipeUnpacker(object):
    SQUOTE_ESCAPE = "%SQ%"
    DQUOTE_ESCAPE = "%DQ%"
    SLASH_ESCAPE = "%SLASH%"
    TRIPLE_SQUOTE_ESCAPE = "%SQSQSQ%"
    TRIPLE_DQUOTE_ESCAPE = "%DQDQDQ%"
    def __init__(self, dir=None):
        self.dir = dir
        if not self.dir:
            self.dir = os.getcwd()            
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

    def execute(self):
        os.chdir(self.dir)
        for key in globals():
            match = re.match(("^([A-Za-z0-9_]+)_PY$"), key)
            if match:
                file_name = "%s.py" % match.group(1)
                path = os.path.join(self.dir, file_name)
                print "Unpacking %s ..." % path 
                src = globals()[key]
                src = src.replace(RecipeUnpacker.TRIPLE_SQUOTE_ESCAPE, "'''")
                src = src.replace(RecipeUnpacker.TRIPLE_DQUOTE_ESCAPE, '\"\"\"')
                src = src.replace(RecipeUnpacker.SQUOTE_ESCAPE, "'")
                src = src.replace(RecipeUnpacker.DQUOTE_ESCAPE, '\"')
                src = src.replace(RecipeUnpacker.SLASH_ESCAPE, "\\\\")
                open(path, "w").write(src)
        
if __name__ == "__main__":
    print __file__
    RecipeUnpacker().execute()
    raw_input("RecipeUnpacker complete. Press RETURN...") 
"""

    def __init__(self):
        self.cur_dir = ""
        self.recipe_fp = None
        
    def open_recipe(self):
        recipe_dir = os.path.join(self.cur_dir, RecipePacker.RECIPE_DIR)
        if not os.path.exists(recipe_dir):
            os.makedirs(recipe_dir)
        recipe_path = os.path.join(recipe_dir, RecipePacker.RECIPE_PY)
        recipe_fp = open(recipe_path, 'w')
        return recipe_fp
    
    def is_valid_src_file(self, path):
        if os.path.isfile(path):
            dir, file_name = os.path.split(path)
            if file_name[-3:].lower() == ".py":
                if file_name[0] != "_" and  "recipe" not in file_name.lower():
                    return True
        return False
    
    def write_src_file_to_recipe(self, path):
        dir, file_name = os.path.split(path)
        src = open(path, "r").read()
        src = src.replace("'''", RecipePacker.TRIPLE_SQUOTE_ESCAPE)
        src = src.replace('"""', RecipePacker.TRIPLE_DQUOTE_ESCAPE)
        src = src.replace("'", RecipePacker.SQUOTE_ESCAPE)
        src = src.replace('"', RecipePacker.DQUOTE_ESCAPE)
        src = src.replace('\\', RecipePacker.SLASH_ESCAPE)
        global_name = "%s_PY" % file_name[:-3]
        self.recipe_fp.write('%s = """' % global_name)
        self.recipe_fp.write(src)
        self.recipe_fp.write('\n"""\n\n')
    
    def execute(self):
        self.cur_dir = os.getcwd()
        self.recipe_fp = self.open_recipe()
        self.recipe_fp.write(RecipePacker.PROLOG)        
        for file_name in os.listdir(self.cur_dir):
            path = os.path.join(self.cur_dir, file_name)
            if self.is_valid_src_file(path):
                print "Packing %s ..." % path
                self.write_src_file_to_recipe(path)           
        self.recipe_fp.write(RecipePacker.EPILOG)
        self.recipe_fp.close()

if __name__ == "__main__":
    print __file__
    RecipePacker().execute()
    raw_input("RecipePacker complete. Press RETURN...") 
