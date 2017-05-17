import os


def error(message):
    print('\x1b[31m{}\x1b[0m'.format(message))


def check_if_nonempty(path):
    if not os.path.exists(path):
        error('ERROR: %s does not exist' % path)
        return False
    with open(path) as reader:
        data = reader.read().strip()
    if not data:
        error('ERROR: %s is empty' % path)
        return False
    return True


def smoketest():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    if all([
        check_if_nonempty('q1/q1.py'),
        check_if_nonempty('q1/q1.txt'),
        check_if_nonempty('q2/q2.py'),
        check_if_nonempty('q2/q2.txt'),
        check_if_nonempty('q3/q3.py'),
        check_if_nonempty('q3/q3.txt'),
        check_if_nonempty('q4/q4.py'),
        check_if_nonempty('q4/q4.txt'),
        check_if_nonempty('q5/q5.py'),
        check_if_nonempty('q5/q5.txt'),
    ]):
        print('smoketest seems cool')


if __name__ == '__main__':
    smoketest()
