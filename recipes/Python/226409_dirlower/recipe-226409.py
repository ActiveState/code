import os
import shutil

def lower_names(dir):
    assert(os.path.isdir(dir))
    [os.rename( os.path.join( dir, file ),
            os.path.join( dir, file.lower() ))
                            for file in os.listdir(dir)]
def get_dir():
    input = raw_input('Enter Directory Name: ')
    return input

if __name__ == '__main__':
    dir = get_dir()
    lower_names(dir)
