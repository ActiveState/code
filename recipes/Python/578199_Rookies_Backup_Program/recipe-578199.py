import os
import sys

def main():
    try:
        source, destination = sys.argv[1:]
        assert os.path.isdir(source), '<source_directory> is not a directory'
        if os.path.exists(destination):
            assert os.path.isdir(destination), \
                   '<destination_directory> is not a directory'
        else:
            os.makedirs(destination)
        copy(source, destination)
    except Exception, error:
        program = 'USAGE:  %s <source_directory> <destination_directory>' % \
                  os.path.basename(sys.argv[0])
        problem = 'ERROR:  %s' % error
        divider = '=' * max(len(program), len(problem))
        sys.stdout.write('\n%s\n%s\n%s\n' % (program, divider, problem))

def copy(source, destination):
    for name in os.listdir(source):
        source_name = os.path.join(source, name)
        destination_name = os.path.join(destination, name)
        try:
            if os.path.isdir(source_name):
                os.mkdir(destination_name)
                copy(source_name, destination_name)
            elif os.path.isfile(source_name):
                file(destination_name, 'wb').write(
                    file(source_name, 'rb').read())
        except:
            sys.stderr.write('\n%s\n%s\n' % (source_name, destination_name))

if __name__ == '__main__':
    main()
