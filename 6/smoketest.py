import os
import subprocess
import sys
import traceback

import infosec.utils


def error(message):
    print('\x1b[31m{}\x1b[0m'.format(message))


def check_if_nonempty(path):
    if not os.path.exists(path):
        error('ERROR: {} does not exist'.format(path))
        return False
    with open(path) as reader:
        data = reader.read().strip()
    if not data:
        error('ERROR: {} is empty'.format(path))
        return False
    return True


def check_payload(module_path):
    try:
        module = infosec.utils.import_module(module_path)
        payload = module.SolutionServer().get_payload(1234)
    except Exception as e:
        error('Exception generating payload for {}'.format(module_path))
        traceback.print_exc()
        return False

    if not isinstance(payload, (str, bytearray)):
        error('Invalid type for {} payload: type was {}, expected str or bytearray'
            .format(module_path, type(payload)))
        return False

    return True


def check_builds(source, target):
    if not check_if_nonempty(source):
        return False

    try:
        subprocess.check_output('make %s' % target, shell=True)
    except Exception as e:
        error('Exception building %s from %s' % (target, source))
        return False

    return True


def smoketest():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    if all([
        check_payload('q1.py'),
        check_if_nonempty('q1.txt'),
        check_payload('q2.py'),
        check_if_nonempty('q2.txt'),
        check_builds('q2.c', 'q2.template'),
        check_payload('q3.py'),
        check_if_nonempty('q3.txt'),
        check_builds('q3.c', 'q3.template'),
        check_payload('q4.py'),
        check_if_nonempty('q4.txt'),
        check_builds('q4.c', 'q4.template'),
    ]):
        print('smoketest seems cool')


if __name__ == '__main__':
    smoketest()
