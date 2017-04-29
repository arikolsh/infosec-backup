#!/usr/bin/python

import os, socket, struct, sys


HOST = '127.0.0.1'
PORT = 8000


def network_order_uint32(value):
    return struct.pack('>L', value)


def get_payload(message):
    return network_order_uint32(len(message)) + message


def main(message):
    payload = get_payload(message)
    conn = socket.socket()
    conn.connect((HOST, PORT))
    try:
        conn.sendall(payload)
    finally:
        conn.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('USAGE: %s <message>' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    main(message=sys.argv[1])
