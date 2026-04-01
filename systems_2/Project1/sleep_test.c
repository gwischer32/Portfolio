#include <stdio.h>
#include <unistd.h>

int main() {
    printf("Background process started, sleeping 5 seconds...\n");
    sleep(5);
    printf("Background process finished!\n");
    return 0;
}
