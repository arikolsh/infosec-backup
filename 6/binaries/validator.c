#include <stdio.h>
#include <string.h>

#include <openssl/sha.h>

#define LOG(fmt, ...) printf(fmt "\n", ##__VA_ARGS__)

char* invalid_hashes[] = {
    "\x29\x41\x71\xdb\x6b\xce\x62\x7e\x2a\x08\xe8\x2f\x1e\x9e\x86\xa0\x57\x30\x6a\x63",
    "\xa1\x6c\xb2\xde\xcc\x5b\xd4\x10\x50\x70\xbd\xf8\xd4\xf7\xcd\x3a\x3e\x5c\x59\xf2",
    "\x94\x2a\x1a\xc3\x47\xe8\xbb\x5f\xf8\x81\x13\x3d\xd7\x74\x52\x1c\xbe\x00\x91\x02",
};

int check_if_virus(char* path)
{
    FILE* fp;
    int   i;
    int   size;
    char  buff[1024];
    char  hash[SHA_DIGEST_LENGTH] = {0};

    SHA_CTX ctx;
    SHA1_Init(&ctx);

    LOG("validating %s", path);

    if ((fp = fopen(path, "r")) == NULL) {
        perror("fopen");
        return 0;
    }

    while ((size = fread(buff, 1, sizeof(buff), fp)) != 0) {
        SHA1_Update(&ctx, buff, size);
    }

    fclose(fp);

    LOG("finalizing hash");
    SHA1_Final(hash, &ctx);

    for (i = 0; i < sizeof(invalid_hashes) / sizeof(invalid_hashes[0]); i++) {
        if (memcmp(hash, invalid_hashes[i], sizeof(hash)) == 0) {
            return 1;
        }
    }

    return 0;
}
