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


def check_buffer_from_function(module_path, function_name, what, ascii_selector):
    try:
        module = infosec.utils.import_module(module_path)
        function = getattr(module, function_name)
        result = function()
    except Exception as e:
        error('Exception generating {} for {}'.format(what, module_path))
        traceback.print_exc()
        return False

    if not isinstance(result, (str, bytearray)):
        error('Invalid {} type for {}: type was {}, expected str or ' +
            'bytearray'.format(what, module_path, type(result)))
        return False

    if ascii_selector and any(ord(c) >= 0x80 for c in ascii_selector(str(result))):
        error('Your {} in {} contains non-ascii bytes'.format(
            what, module_path))
        return False

    return True


def check_shellcode(module_path, ascii=False):
    return check_buffer_from_function(module_path, 'get_shellcode', 'shellcode',
        (lambda str: str) if ascii else None)


def check_payload(module_path, ascii=False):
    return check_buffer_from_function(module_path, 'get_payload', 'payload',
        (lambda str: str[4:-4]) if ascii else None)


def smoketest():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    if all([
        check_if_nonempty('q1.txt'),
        check_if_nonempty('q1.py'),
        check_payload('q1.py'),
        check_if_nonempty('shellcode.asm'),
        check_if_nonempty('q2.py'),
        check_payload('q2.py'),
        check_shellcode('q2.py'),
        check_if_nonempty('q2.txt'),
        check_if_nonempty('q3.txt'),
        check_if_nonempty('q3.py'),
        check_payload('q3.py', ascii=True),
        check_shellcode('q3.py', ascii=True),
    ]):
        print('smoketest seems cool')


if __name__ == '__main__':
    smoketest()
