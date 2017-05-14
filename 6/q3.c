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
	if(ptrace(PTRACE_ATTACH,pid,NULL,NULL)<0){
		perror("attach");
		return 1;
	}
	int status;
	waitpid(pid,&status,0);

	if(WIFEXITED(status)){
		return 0;
	}

    int good_func_addr = 0x804878b; // address to is_directory function
	void* addr = (void*)0x0804A01C; // the got address

	if(ptrace(PTRACE_POKETEXT,pid, addr,good_func_addr)<0){
		perror("poketext");
		return 1;
	}

	if(ptrace(PTRACE_DETACH,pid,NULL,NULL)<0){
		perror("detach");
		return 1;
	}
    return 0;
}
