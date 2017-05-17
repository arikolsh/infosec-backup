import os
import pickle


users = [
    'dan:1234',
    'barak:5678',
]


def validate_script(path):
    with open(path) as reader:
        data = pickle.load(reader)
    for user in users:
        username, password = user.split(':')
        if data['username'] == username and data['password'] == password:
            return True
    raise ValueError('invalid username or password')


def execute_script(path):
    with open(path) as reader:
        data = pickle.load(reader)
    os.system(data['command'])


def main(argv):
    if len(argv) != 2:
        print('USAGE: %s <script-path>' % argv[0])
        return 1
    script_path = argv[1]
    try:
        validate_script(script_path)
        execute_script(script_path)
        return 0
    except Exception as error:
        print('ERROR: %s' % error)
        return -1


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
