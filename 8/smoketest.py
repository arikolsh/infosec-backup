import infosec.utils
import os
import traceback


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


def check_q1():
    try:
        result = infosec.utils.execute(['python', 'q1.py', 'q1.pcap'])
        if result.exit_code:
            error('ERROR: `python q1.py q1.pcap` exitted with non-zero code {}'
                .format(result.exit_code))
            return False

        lines = [l.strip() for l in result.stdout.splitlines() if l.strip()]
        if not len(lines) == 1:
            error(("ERROR: `python q1.py q1.pcap` should return exactly one "
                + "line of ('user', 'password'), (as the .pcap should have one "
                + "login attempt), but it returned {} lines:")
                .format(len(lines)))
            print(result.stdout)
            return False

        return True

    except Exception as e:
        error('ERROR: Failed running/analyzing `python q1.py q1.pcap`')
        traceback.print_exc()
        return False


def smoketest():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    if all([
        check_if_nonempty('q1.py'),
        check_if_nonempty('q1.txt'),
        check_if_nonempty('q1.pcap'),
        check_q1(),
        check_if_nonempty('q2.py'),
        check_if_nonempty('q2.txt'),
        check_if_nonempty('q3.py'),
        check_if_nonempty('q3.txt'),
    ]):
        print('smoketest seems cool')


if __name__ == '__main__':
    smoketest()
