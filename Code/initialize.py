import os
import sys


def find_exec(path):
    for root, dirs, files in os.walk(path):
        if 'git.exe' in files:
            return os.path.join(root, 'git.exe')

def add_path(path):
    try:
        sys.path.index(path)
    except ValueError:
        os.environ['PATHPYTHON'] = path

def main():
    exec_path = find_exec(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    add_path(exec_path)
    print(sys.path)



if __name__ == '__main__':
    main()
