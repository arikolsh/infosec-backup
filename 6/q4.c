#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/ptrace.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <sys/user.h>

int pid = 0x12345678;
int READ_SYSCALL_NUM = 3;

int main() {
        // Make the malware stop waiting for our output by forking a child process:
    if (fork() != 0) {
        // Kill the parent process so we stop waiting from the malware
        return 0;
    } else {
        // Close the output stream so we stop waiting from the malware
        fclose(stdout);
    }

    int res;
    res= ptrace(PTRACE_ATTACH, pid, NULL, NULL); //attach tracer to pid
    if(res < 0){
        perror("attach");
        return 1;
    }
    int status=0;
    struct user_regs_struct regs; //registers struct
    while (waitpid(pid, &status, 0) && !WIFEXITED(status)) {
        ptrace(PTRACE_GETREGS, pid, NULL, &regs); //put registers' data in regs
        if (regs.orig_eax == READ_SYSCALL_NUM) {
            regs.edx = 0; //put 0 in length
            ptrace(PTRACE_SETREGS, pid, NULL, &regs); //set registers
        }
        ptrace(PTRACE_SYSCALL, pid, NULL, NULL); //continue and stop right before the system call
    }

    return 0;
}

