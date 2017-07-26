import sys
import os

def main():
    # Process old and new path names.
    old_path = sys.argv[0]
    root, file = os.path.split(old_path)
    name, extension = os.path.splitext(file)
    new_path = os.path.join(root, str(int(name) + 1) + extension)
    # Start a new program generation.
    with open(old_path, 'rb') as old_file, open(new_path, 'wb') as new_file:
        new_file.write(old_file.read())
    os.remove(old_path)
    os.startfile(new_path)

if __name__ == '__main__':
    main()
