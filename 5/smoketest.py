import os
import shutil
import subprocess
import sys
import traceback

import infosec.utils


TEST_COMMAND = 'echo "I am g`whoami`!"; exit'
COMMAND_RESULT = 'I am groot!'


PATH_TO_SUDO = './sudo'


def error(message):
    print('\x1b[31m{}\x1b[0m'.format(message))


def check_arg_from_function(module_path, function_name):
    try:
        module = infosec.utils.import_module(module_path)
        function = getattr(module, function_name)
        result = function()
    except Exception as e:
        error('Exception generating argument for {}'.format(module_path))
        traceback.print_exc()
        return False, None

    if not isinstance(result, str):
        error('Invalid {} type for argument: type was {}, expected str'.format(
            module_path, type(result)))
        return False, None

    return True, result


def check_q1a():
    if os.path.isfile('core'):
        os.remove('core')
    success, arg = check_arg_from_function('q1a.py', 'get_crash_arg')
    if not success:
        return False
    result = infosec.utils.execute([PATH_TO_SUDO, arg])
    if not os.path.exists('core'):
        error('ERROR: Running q1a.py did not generate a `core` file!')
        return False
    return True


def check_q1b():
    success, arg = check_arg_from_function('q1b.py', 'get_arg')
    if not success:
        return False
    result = infosec.utils.execute([PATH_TO_SUDO, arg], TEST_COMMAND)
    if COMMAND_RESULT not in result.stdout:
        error('ERROR: Failed running a root command shell using q1b.py!')
        return False
    return True


def check_q1c():
    success, arg = check_arg_from_function('q1c.py', 'get_arg')
    if not success:
        return False
    result = infosec.utils.execute([PATH_TO_SUDO, arg], TEST_COMMAND)
    if COMMAND_RESULT not in result.stdout:
        error('ERROR: Failed running a root command shell using q1c.py!')
        return False
    if result.exit_code != 0x42:
        error('ERROR: The shell did not exit with a code of 0x42 (66)!')
        return False
    return True


def check_q3():
    success, arg = check_arg_from_function('q3.py', 'get_arg')
    if not success:
        return False

    prefix = 'auth='
    result = infosec.utils.execute([
        '/usr/bin/gdb', '--batch',
        '-ex', 'run', '-ex', 'printf "{}%d\n", auth'.format(prefix),
        '--args', PATH_TO_SUDO, arg])

    if prefix not in result.stdout:
        error('ERROR: Failed debugging sudo with the argument from q3.py!')
        return False

    auth_line = result.stdout[result.stdout.find(prefix):].splitlines()[0]
    auth = int(auth_line[len(prefix):])

    if auth == 0:
        error('ERROR: Debugging your q3.py, it seems auth is stil 0!')
        return False

    return True


def check_q4():
    success, arg = check_arg_from_function('q4.py', 'get_arg')
    if not success:
        return False

    current_user_sudo = os.path.join(os.path.dirname(PATH_TO_SUDO), 'sudo_smoketest')
    try:
        shutil.copy(PATH_TO_SUDO, current_user_sudo)
        result = infosec.utils.execute([current_user_sudo, arg], timeout=0.05)
        lines = result.stdout.strip().splitlines()
        if len(lines) < 10:
            error('ERROR: Failed getting a large amount of lines with q4.py!')
            return False
        if not any('to your leader!' in line for line in lines):
            error('ERROR: Failed finding a call to your leader in the output from q4.py!')
            return False
        return True
    finally:
        if os.path.isfile(current_user_sudo):
            os.remove(current_user_sudo)


def check_q_search():
    try:
        search = infosec.utils.import_module('search.py')
        gs = search.GadgetSearch('libc.bin', 0x123)
    except Exception as e:
        error('ERROR: Failed loading the gadget search engine')
        traceback.print_exc()
        return False

    try:
        regs = ('esi', 'edi')
        gadget_format = 'MOV {0}, {1}'
        expected = set([
            gadget_format.format(reg1, reg2)
            for reg1 in regs
            for reg2 in regs
        ])
        cmds = gs.format_all_gadgets('MOV {0}, {1}', ('esi', 'edi'))
        if not set(cmds) == set(expected):
            error('ERROR: Unexpected output with format_all_gadgets!')
            print('Expected: {}, Actual: {}'.format(expected, actual))
            return False
    except Exception as e:
        error('ERROR: Failed using the gadget search engine')
        traceback.print_exc()
        return False
    return True


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


def smoketest():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    if all([
        check_q1a(),
        check_q1b(),
        check_q1c(),
        check_q_search(),
        check_q3(),
        check_q4(),
        check_if_nonempty('libc.bin'),
        check_if_nonempty('q1a.txt'),
        check_if_nonempty('q1b.txt'),
        check_if_nonempty('q1c.txt'),
        check_if_nonempty('q3.txt'),
        check_if_nonempty('q4.txt'),
    ]):
        print('smoketest seems cool')


if __name__ == '__main__':
    smoketest()
