#!/usr/bin/python

import subprocess


ASSEMBLY_TEMPLATE = '''
.intel_syntax noprefix
.globl main
main:
%s
'''


ASSEMBLE = 'gcc -xassembler - -o /dev/stdout -m32 -nostdlib -emain -Xlinker --oformat=binary'


def run(command, stdin):
    proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = proc.communicate(stdin)
    if stderr:
        raise RuntimeError(stderr)
    return stdout


def assemble_data(data):
    return run(ASSEMBLE, ASSEMBLY_TEMPLATE % data)
    

def assemble_file(path):
    return assemble_data(open(path, 'rb').read())


def main(path=None, assembly=None, ascii=False):
    try:
        assembly = assemble_file(path) if path else assemble_data(assembly)
        if ascii:
            output = []
            for c in assembly:
                n = ord(c)
                if n > 0x80:
                    output.append('\x1b[31m\\x%02x\x1b[0m' % n)
                else:
                    output.append('\\x%02x' % n)
            print('"%s"' % ''.join(output))
        else:
            print(repr(assembly))
    except RuntimeError as error:
        print(error)


if __name__ == '__main__':
    import os, sys

    ascii = False
    direct = False

    if '--help' in sys.argv or len(sys.argv) < 2:
        name = os.path.basename(sys.argv[0])
        print('USAGE:')
        print('\t%s [--ascii] <file>' % name)
        print('\t%s [--ascii] --direct <assembly-str>' % name)
        sys.exit(1)

    for arg in sys.argv[1:-1]:
        if arg == '--ascii':
            ascii = True
        elif arg == '--direct':
            direct = True
        else:
            print('Ignoring unrecognized flag %s' % arg)

    if direct:
        main(assembly=sys.argv[-1], ascii=ascii)
    else:
        main(path=sys.argv[-1], ascii=ascii)
