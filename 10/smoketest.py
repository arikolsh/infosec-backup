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


def check_solution(question):
    msg = question + '.msg'
    console = question + '.console'
    if os.path.exists(msg):
        if os.path.exists(console):
            error('ERROR: Both .msg and .console found for %s' % question)
            return False
        path = msg
    elif os.path.exists(console):
        path = console
    else:
        error('ERROR: No solution provided for %s' % question)
        return False
    return check_if_nonempty(path)

def smoketest():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    if all([
        check_solution('q1'),
        check_if_nonempty('q1.txt'),
        check_solution('q2'),
        check_if_nonempty('q2.txt'),
        check_solution('q3'),
        check_if_nonempty('q3.txt'),
        check_solution('q4'),
        check_if_nonempty('q4.txt'),
        check_if_nonempty('q5.html'),
        check_if_nonempty('q5.txt'),
    ]):
        print('smoketest seems cool')


if __name__ == '__main__':
    smoketest()
