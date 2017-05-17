import json
import os
import re

from Crypto.Hash      import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


keys = [
    '-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC05QMiy2ib1kxDdnTy9nXgbQuq\nniprmnRpxrGLqq9AlY+djyugzq0GRlMzlRKhxeFbp/jJ4MO+3Np9yytKP7UIs+xF\niTgFuLCVdVpJItjxXEfvCLQHUZ0/ckwvqfAN72XJKoSV5/xo6N9Z5iKLkHl0Dcf4\nmDQVAWRypqZLeWdNKwIDAQAB\n-----END PUBLIC KEY-----',
    '-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDSCHWMrl+aHU4KrMgCZgc+BvXJ\nn7xjo2LiAvAbw3W2y2PD0SQjrVf0RCS/syV6o2BmNUvpkiad4gyGGHCim8wIsjRC\nEOCf2wVDSOF9XG4XY4ngzqHSrbX9bfgo409pGBkpvriGfNva9OmJ2T6Qu3y3Y5eN\nRoHZqiDL3+KbniQ+owIDAQAB\n-----END PUBLIC KEY-----',
]


def verify(public_key, data, signature):
    public_key = RSA.importKey(public_key)
    signer     = PKCS1_v1_5.new(public_key)
    hasher     = SHA256.new(data)
    for _ in range(1000000):
        hasher = SHA256.new(hasher.digest())
    return signer.verify(hasher, signature)


def validate_script(path):
    with open(path) as reader:
        data = json.load(reader)
    for key in keys:
        if verify(key, data['command'], data['signature'].decode('hex')):
            return True
    raise ValueError('invalid signature')


def execute_script(path):
    with open(path) as reader:
        data = json.load(reader)
    os.system(data['command'])


def main(argv):
    if len(argv) != 2:
        print('USAGE: %s <script-path>' % argv[0])
        return 1
    script_path = argv[1]
    try:
        validate_script(script_path)
        execute_script(script_path)
        return 0
    except Exception as error:
        print('ERROR: %s' % error)
        return -1


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
