import os

# i am big on absolute paths, so i made it return an absolute path
# also that makes the results clearer.
def full_path(dir_):
    if dir_[0] == '~' and not os.path.exists(dir_):
        dir_ = os.path.expanduser(dir_)
    return os.path.abspath(dir_)

if __name__ == '__main__':
    print os.path.abspath(full_path('~/test')) # returns /home/rv/~/test if it exists or else it outputs /home/rv/test
