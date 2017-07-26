    import os
    import sys


    def create_tree_structure(rootpath):
        rootpath = rootpath.rstrip(os.sep)
        start_level = rootpath.count(os.sep)
        for root, dirs, files in os.walk(rootpath):
            present_level = root.count(os.sep)
            actual_level = present_level - start_level
            spacing = (actual_level) * ' '
            file_list = [file for file in files]
            sys.stdout.write(spacing + '-' + os.path.basename(root) + ' ' +
                             str(file_list) + '\n')

    if __name__ == '__main__':
        create_tree_structure('../path')
