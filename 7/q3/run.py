import os


users = [
    'dan:1234',
    'barak:5678',
]


def validate_script(path):
    with open(path) as reader:
        data = reader.read()
    if data.count(':') < 2:
        raise ValueError('invalid script format')
    username_end = data.index(':')
    password_end = data.index(':', username_end + 1)
    for user in users:
        if (
            user[:username_end] == data[:username_end] and
            user[username_end + 1:password_end] == data[username_end + 1:password_end]
        ):
            return True
    raise ValueError('invalid username or password')


def execute_script(path):
    with open(path) as reader:
        data = reader.read()
    command_start = data.index(':', data.index(':') + 1) + 1
    os.system(data[command_start:])


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
