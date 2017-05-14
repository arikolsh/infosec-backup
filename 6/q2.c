#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/ptrace.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <stdlib.h>

int pid = 0x12345678;

int main() {
	if(ptrace(PTRACE_ATTACH,pid,NULL,NULL)==-1){
		perror("attach");
		return 1;
	}
	int status;
	waitpid(pid,&status,0);
	if(WIFEXITED(status)){
		return 0;
	}
	int my_func = 0xc3c031; //xor eax, eax;
	void* check_if_pass_addr = (void*)0xb7fd3750;
	if(ptrace(PTRACE_POKETEXT,pid, check_if_pass_addr,my_func)){
		perror("poketext");
		return 1;
	}

	if(ptrace(PTRACE_DETACH,pid,NULL,NULL)==-1){
		perror("detach");
		return 1;
	}
    return 0;
}
